import os
from typing import Optional

class Settings:
    # Get environment variables with validation
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production-32")
    AES_KEY: str = os.getenv("AES_KEY", "fallback-32-byte-key-for-aes-256!")
    
    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data_leak_prevention.db")
    
    # JWT Settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security Settings
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_TIME: int = 900  # 15 minutes in seconds
    
    # SQL Injection Patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|ALTER|CREATE|TRUNCATE)\b)",
        r"(\b(OR|AND)\b\s*\d+\s*=\s*\d+)",
        r"(--|\#|\/\*)",
        r"(\b(WAITFOR|DELAY)\b)",
        r"(\b(XP_|SP_)\w+)",
        r"(;\s*\w+;)",
        r"(\b(LOAD_FILE|INTO_FILE|OUTFILE)\b)",
        r"(\b(BENCHMARK|SLEEP)\b\s*\()",
    ]

    def __init__(self):
        self._validate_keys()
    
    def _validate_keys(self):
        """Validate and ensure proper key lengths"""
        # Ensure AES key is exactly 32 bytes
        if len(self.AES_KEY) != 32:
            print(f"⚠️  AES key is {len(self.AES_KEY)} characters, padding/truncating to 32 characters")
            # Pad with '!' or truncate to 32 characters
            self.AES_KEY = self.AES_KEY.ljust(32, '!')[:32]
        
        # Warn about default secrets
        if "fallback" in self.SECRET_KEY or "fallback" in self.AES_KEY:
            print("🚨 WARNING: Using fallback keys! Generate proper keys for production.")

settings = Settings()