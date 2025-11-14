import pytest
from app.security import AESEncryption, SQLInjectionDetector, DoubleLayerSecurity

def test_aes_encryption():
    """Test AES encryption and decryption"""
    aes = AESEncryption()
    test_data = "Sensitive user data"
    
    encrypted = aes.encrypt(test_data)
    decrypted = aes.decrypt(encrypted)
    
    assert decrypted == test_data
    assert encrypted != test_data

def test_sql_injection_detection():
    """Test SQL injection detection"""
    detector = SQLInjectionDetector()
    
    # Test malicious inputs
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "1' OR '1'='1",
        "UNION SELECT username, password FROM users",
        "admin' --",
        "'; EXEC xp_cmdshell('format c:'); --"
    ]
    
    for malicious_input in malicious_inputs:
        assert detector.detect_sql_injection(malicious_input) == True
    
    # Test safe inputs
    safe_inputs = [
        "john_doe",
        "normal password",
        "user@example.com",
        "John Doe",
        "+1234567890"
    ]
    
    for safe_input in safe_inputs:
        assert detector.detect_sql_injection(safe_input) == False

def test_double_layer_security():
    """Test double layer security"""
    security = DoubleLayerSecurity()
    
    # Test user data validation and encryption
    user_data = {
        "email": "user@example.com",
        "password": "secure_password",
        "ssn": "123-45-6789"
    }
    
    encrypted_data = security.validate_and_encrypt_user_data(user_data)
    
    assert "email" in encrypted_data
    assert encrypted_data["email"] != user_data["email"]
    assert "ssn" in encrypted_data
    assert encrypted_data["ssn"] != user_data["ssn"]

if __name__ == "__main__":
    test_aes_encryption()
    test_sql_injection_detection()
    test_double_layer_security()
    print("All security tests passed!")