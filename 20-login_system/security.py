import hashlib
import secrets
import os
from typing import Tuple

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """Hash a password with a randomly generated salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # Number of iterations
        )
        return salt, password_hash.hex()
    
    @staticmethod
    def verify_password(password: str, salt: str, stored_hash: str) -> bool:
        """Verify a password against stored hash and salt"""
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return password_hash.hex() == stored_hash
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username requirements"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if len(username) > 20:
            return False, "Username must be less than 20 characters"
        if not username.isalnum():
            return False, "Username can only contain letters and numbers"
        return True, "Valid username"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if len(password) > 50:
            return False, "Password must be less than 50 characters"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter"
        return True, "Valid password"