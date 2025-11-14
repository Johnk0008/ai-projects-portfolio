from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.security import SQLInjectionDetector

sql_detector = SQLInjectionDetector()

class UserCreate(BaseModel):
    username: str
    email: str  # Changed from EmailStr to str to avoid email-validator dependency
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if sql_detector.detect_sql_injection(v):
            raise ValueError('Username contains potential SQL injection patterns')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if v and sql_detector.detect_sql_injection(v):
            raise ValueError('Email contains potential SQL injection patterns')
        # Basic email format check without external dependency
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if v and sql_detector.detect_sql_injection(v):
            raise ValueError('Full name contains potential SQL injection patterns')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and sql_detector.detect_sql_injection(v):
            raise ValueError('Phone contains potential SQL injection patterns')
        return v

class UserLogin(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if sql_detector.detect_sql_injection(v):
            raise ValueError('Username contains potential SQL injection patterns')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class SecureQuery(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None
    
    @validator('query')
    def validate_query(cls, v):
        if sql_detector.detect_sql_injection(v):
            raise ValueError('Query contains potential SQL injection patterns')
        return v

class SecurityEventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source_ip: Optional[str]
    description: str
    timestamp: datetime
    mitigated: bool
    
    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None