from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import logging

from app.database import get_db, User, AuditLog, SecurityEvent
from app.models import UserCreate, UserLogin, UserResponse, SecureQuery, APIResponse
from app.security import security, SQLInjectionDetector

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
sql_detector = SQLInjectionDetector()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def log_audit_event(db: Session, user_id: int, action: str, description: str, 
                   request: Request, success: bool = True):
    """Log audit event to database"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=success,
            timestamp=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to log audit event: {str(e)}")

@router.post("/register", response_model=APIResponse)
async def register_user(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Register new user with encrypted sensitive data"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Encrypt sensitive user data
        encrypted_data = security.validate_and_encrypt_user_data({
            "email": user_data.email,
            "full_name": user_data.full_name,
            "phone": user_data.phone
        })
        
        # Create new user
        new_user = User(
            username=user_data.username,
            email_encrypted=encrypted_data["email"],
            password_hash=get_password_hash(user_data.password),
            full_name_encrypted=encrypted_data.get("full_name"),
            phone_encrypted=encrypted_data.get("phone"),
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Log audit event
        log_audit_event(
            db, new_user.id, "user_registration", 
            f"User {user_data.username} registered successfully", request, True
        )
        
        return APIResponse(
            success=True,
            message="User registered successfully",
            data={"user_id": new_user.id}
        )
        
    except ValueError as e:
        log_audit_event(db, None, "user_registration", str(e), request, False)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log_audit_event(db, None, "user_registration", f"Registration failed: {str(e)}", request, False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=APIResponse)
async def login_user(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """User login with brute force protection"""
    try:
        # Find user
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user:
            log_audit_event(db, None, "login_attempt", f"Failed login for non-existent user: {login_data.username}", request, False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if account is locked
        if user.is_locked:
            lock_time_remaining = (user.last_login + timedelta(minutes=15)) - datetime.utcnow()
            if lock_time_remaining.total_seconds() > 0:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account temporarily locked due to too many failed attempts"
                )
            else:
                # Unlock account
                user.is_locked = False
                user.login_attempts = 0
                db.commit()
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            user.login_attempts += 1
            
            # Lock account after too many attempts
            if user.login_attempts >= 5:
                user.is_locked = True
                user.last_login = datetime.utcnow()
                db.commit()
                
                log_audit_event(db, user.id, "account_locked", "Account locked due to too many failed login attempts", request, False)
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account locked due to too many failed attempts"
                )
            
            db.commit()
            log_audit_event(db, user.id, "login_attempt", "Failed login attempt", request, False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Successful login
        user.login_attempts = 0
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Decrypt user data for response
        decrypted_email = security.aes.decrypt(user.email_encrypted)
        decrypted_full_name = security.aes.decrypt(user.full_name_encrypted) if user.full_name_encrypted else None
        decrypted_phone = security.aes.decrypt(user.phone_encrypted) if user.phone_encrypted else None
        
        log_audit_event(db, user.id, "login", "User logged in successfully", request, True)
        
        return APIResponse(
            success=True,
            message="Login successful",
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": decrypted_email,
                    "full_name": decrypted_full_name,
                    "phone": decrypted_phone,
                    "is_active": user.is_active
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_audit_event(db, None, "login_attempt", f"Login failed: {str(e)}", request, False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/secure-query", response_model=APIResponse)
async def execute_secure_query(query_data: SecureQuery, request: Request, db: Session = Depends(get_db)):
    """Execute secure SQL query with injection protection"""
    try:
        # Double-layer security validation
        secure_execution = security.secure_sql_execution(
            query_data.query, 
            query_data.parameters or {}
        )
        
        # In a real implementation, this would execute the actual query
        # For demonstration, we're returning the secure execution plan
        
        log_audit_event(
            db, None, "secure_query_execution", 
            f"Secure query executed: {query_data.query[:100]}...", request, True
        )
        
        return APIResponse(
            success=True,
            message="Query executed securely",
            data=secure_execution
        )
        
    except ValueError as e:
        log_audit_event(
            db, None, "secure_query_blocked", 
            f"Query blocked due to security concerns: {str(e)}", request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log_audit_event(
            db, None, "secure_query_error", 
            f"Query execution error: {str(e)}", request, False
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/security-events", response_model=APIResponse)
async def get_security_events(
    request: Request, 
    db: Session = Depends(get_db),
    severity: str = None,
    event_type: str = None,
    limit: int = 50
):
    """Get security events (admin function)"""
    try:
        query = db.query(SecurityEvent)
        
        if severity:
            query = query.filter(SecurityEvent.severity == severity)
        if event_type:
            query = query.filter(SecurityEvent.event_type == event_type)
        
        events = query.order_by(SecurityEvent.timestamp.desc()).limit(limit).all()
        
        log_audit_event(db, None, "view_security_events", "Security events viewed", request, True)
        
        return APIResponse(
            success=True,
            message="Security events retrieved",
            data={"events": [
                {
                    "id": event.id,
                    "event_type": event.event_type,
                    "severity": event.severity,
                    "source_ip": event.source_ip,
                    "description": event.description,
                    "timestamp": event.timestamp,
                    "mitigated": event.mitigated
                } for event in events
            ]}
        )
        
    except Exception as e:
        log_audit_event(db, None, "view_security_events", f"Failed to retrieve security events: {str(e)}", request, False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/test-sql-injection")
async def test_sql_injection_detection(request: Request, input: str = ""):
    """Test endpoint to demonstrate SQL injection detection"""
    if sql_detector.detect_sql_injection(input):
        return APIResponse(
            success=False,
            message="SQL injection detected and blocked!",
            data={"input": input, "blocked": True}
        )
    else:
        return APIResponse(
            success=True,
            message="Input is safe",
            data={"input": input, "blocked": False}
        )