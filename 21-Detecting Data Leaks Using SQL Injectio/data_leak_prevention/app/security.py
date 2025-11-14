import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import re
from typing import Optional
from config import settings

class AESEncryption:
    def __init__(self):
        # Ensure key is exactly 32 bytes
        self.key = settings.AES_KEY.encode('utf-8')
        if len(self.key) != 32:
            # Pad with zeros or truncate to 32 bytes
            self.key = self.key.ljust(32, b'\0')[:32]
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using AES-256 in CBC mode"""
        try:
            # Generate random IV
            iv = os.urandom(16)
            
            # Create cipher
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Pad the data
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
            
            # Encrypt
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            # Combine IV and encrypted data
            combined = iv + encrypted
            
            # Return base64 encoded string
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt AES-256 encrypted text"""
        try:
            # Decode base64
            combined = base64.b64decode(encrypted_text.encode('utf-8'))
            
            # Extract IV and encrypted data
            iv = combined[:16]
            encrypted = combined[16:]
            
            # Create cipher
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # Decrypt
            decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
            
            # Unpad
            unpadder = padding.PKCS7(128).unpadder()
            decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            return decrypted.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

class SQLInjectionDetector:
    def __init__(self):
        # Use the patterns from settings
        self.patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|ALTER|CREATE|TRUNCATE)\b)",
            r"(\b(OR|AND)\b\s*\d+\s*=\s*\d+)",
            r"(--|\#|\/\*)",
            r"(\b(WAITFOR|DELAY)\b)",
            r"(\b(XP_|SP_)\w+)",
            r"(;\s*\w+;)",
            r"(\b(LOAD_FILE|INTO_FILE|OUTFILE)\b)",
            r"(\b(BENCHMARK|SLEEP)\b\s*\()",
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.patterns]
    
    def detect_sql_injection(self, input_string: str) -> bool:
        """Detect SQL injection patterns in input string"""
        if not input_string:
            return False
        
        # Check for common SQL injection patterns
        for pattern in self.compiled_patterns:
            if pattern.search(input_string):
                return True
        
        # Additional heuristic checks
        suspicious_sequences = [
            "1=1", "1=2", "' OR '1'='1", "' OR '1'='1'--", 
            "';", "\" OR \"\"=\"", " OR ", " AND ", " UNION ", " SELECT "
        ]
        
        input_lower = input_string.lower()
        for seq in suspicious_sequences:
            if seq.lower() in input_lower:
                return True
        
        return False
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize input by removing potentially dangerous characters"""
        if not input_string:
            return ""
        
        # Remove or escape dangerous characters
        sanitized = input_string
        dangerous_chars = ["'", "\"", ";", "--", "/*", "*/", "#"]
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized.strip()

class DoubleLayerSecurity:
    def __init__(self):
        self.aes = AESEncryption()
        self.sql_detector = SQLInjectionDetector()
        self.login_attempts = {}
    
    def validate_and_encrypt_user_data(self, user_data: dict) -> dict:
        """First layer: Validate input and encrypt sensitive data"""
        encrypted_data = {}
        
        for key, value in user_data.items():
            if value is None:
                encrypted_data[key] = None
                continue
                
            if isinstance(value, str):
                # Check for SQL injection
                if self.sql_detector.detect_sql_injection(value):
                    raise ValueError(f"Potential SQL injection detected in field: {key}")
                
                # Encrypt sensitive fields
                if key.lower() in ['password', 'email', 'ssn', 'credit_card', 'phone']:
                    encrypted_data[key] = self.aes.encrypt(value)
                else:
                    encrypted_data[key] = value
            else:
                encrypted_data[key] = value
        
        return encrypted_data
    
    def secure_sql_execution(self, query: str, params: dict = None) -> dict:
        """Second layer: Secure SQL execution with parameterized queries"""
        if self.sql_detector.detect_sql_injection(query):
            raise ValueError("Potential SQL injection detected in query")
        
        # Simulate secure parameterized query execution
        secure_query = self._create_parameterized_query(query, params or {})
        
        return {
            "secure_query": secure_query,
            "is_safe": True,
            "execution_context": "restricted"
        }
    
    def _create_parameterized_query(self, query: str, params: dict) -> str:
        """Create a parameterized query to prevent SQL injection"""
        # This is a simplified version - in production, use proper ORM parameterization
        sanitized_params = {}
        for key, value in params.items():
            if isinstance(value, str):
                sanitized_params[key] = self.sql_detector.sanitize_input(value)
            else:
                sanitized_params[key] = value
        
        # In a real implementation, this would use proper database driver parameterization
        return f"EXECUTE SECURE QUERY WITH PARAMS: {sanitized_params}"

# Create security instance
security = DoubleLayerSecurity()