from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import logging
from app.database import SessionLocal, SecurityEvent
from app.security import SQLInjectionDetector
from datetime import datetime

sql_detector = SQLInjectionDetector()

class SecurityMiddleware:
    def __init__(self):
        self.rate_limit_requests = {}
        self.rate_limit_window = 60  # 1 minute window
        self.max_requests_per_minute = 100
    
    async def process_request(self, request: Request, call_next):
        # Check rate limiting
        client_ip = request.client.host if request.client else "unknown"
        
        if self._is_rate_limited(client_ip):
            return JSONResponse(
                status_code=429,
                content={"success": False, "message": "Rate limit exceeded"}
            )
        
        # Check for SQL injection in query parameters
        query_params = dict(request.query_params)
        for param, value in query_params.items():
            if sql_detector.detect_sql_injection(str(value)):
                await self._log_security_event(
                    "sql_injection",
                    "high",
                    client_ip,
                    f"SQL injection detected in query parameter: {param}",
                    str(value)
                )
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "message": "Potential SQL injection detected"}
                )
        
        # Check for SQL injection in path parameters
        path_params = request.path_params
        for param, value in path_params.items():
            if sql_detector.detect_sql_injection(str(value)):
                await self._log_security_event(
                    "sql_injection",
                    "high",
                    client_ip,
                    f"SQL injection detected in path parameter: {param}",
                    str(value)
                )
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "message": "Potential SQL injection detected"}
                )
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if client IP is rate limited"""
        current_time = time.time()
        if client_ip not in self.rate_limit_requests:
            self.rate_limit_requests[client_ip] = []
        
        # Remove requests outside the current window
        self.rate_limit_requests[client_ip] = [
            req_time for req_time in self.rate_limit_requests[client_ip]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Check if over limit
        if len(self.rate_limit_requests[client_ip]) >= self.max_requests_per_minute:
            return True
        
        # Add current request
        self.rate_limit_requests[client_ip].append(current_time)
        return False
    
    async def _log_security_event(self, event_type: str, severity: str, source_ip: str, 
                                description: str, payload: str = None):
        """Log security event to database"""
        try:
            db = SessionLocal()
            security_event = SecurityEvent(
                event_type=event_type,
                severity=severity,
                source_ip=source_ip,
                description=description,
                payload=payload,
                timestamp=datetime.utcnow()
            )
            db.add(security_event)
            db.commit()
        except Exception as e:
            logging.error(f"Failed to log security event: {str(e)}")
        finally:
            db.close()

security_middleware = SecurityMiddleware()