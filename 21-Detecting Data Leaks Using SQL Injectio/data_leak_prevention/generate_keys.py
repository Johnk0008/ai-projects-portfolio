#!/usr/bin/env python3
"""
Secure Key Generation Script for Data Leak Prevention System
"""

import secrets
import base64
import os
from cryptography.fernet import Fernet

def generate_secret_key(length=32):
    """Generate a secure secret key for JWT tokens"""
    return secrets.token_urlsafe(length)

def generate_aes_key():
    """Generate a secure 32-byte AES key"""
    return secrets.token_urlsafe(32)

def generate_fernet_key():
    """Generate a Fernet key for additional encryption"""
    return Fernet.generate_key().decode()

def generate_all_keys():
    """Generate all required keys"""
    print("🔐 Generating Secure Keys for Data Leak Prevention System")
    print("=" * 60)
    
    # Generate keys
    secret_key = generate_secret_key()
    aes_key = generate_aes_key()[:32]  # Ensure exactly 32 bytes
    fernet_key = generate_fernet_key()
    
    print("✅ Generated Keys:")
    print(f"SECRET_KEY={secret_key}")
    print(f"AES_KEY={aes_key}")
    print(f"FERNET_KEY={fernet_key}")
    print(f"DATABASE_URL=sqlite:///./data_leak_prevention.db")
    
    print("\n📝 Environment File Content (.env):")
    print("=" * 40)
    env_content = f"""SECRET_KEY={secret_key}
AES_KEY={aes_key}
FERNET_KEY={fernet_key}
DATABASE_URL=sqlite:///./data_leak_prevention.db
DEBUG=False
HOST=0.0.0.0
PORT=8000
"""
    print(env_content)
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Keys saved to .env file")
    print("🔒 Remember to keep these keys secure and never commit them to version control!")
    
    return secret_key, aes_key, fernet_key

def verify_key_lengths():
    """Verify that all keys meet length requirements"""
    print("\n🔍 Verifying Key Lengths:")
    print("=" * 40)
    
    secret_key = generate_secret_key()
    aes_key = generate_aes_key()[:32]
    
    print(f"SECRET_KEY length: {len(secret_key)} characters")
    print(f"AES_KEY length: {len(aes_key)} bytes")
    print(f"AES_KEY value: {aes_key}")
    
    # Verify AES key is exactly 32 bytes
    if len(aes_key.encode('utf-8')) == 32:
        print("✅ AES key is exactly 32 bytes - Perfect!")
    else:
        print("❌ AES key length issue detected")
        # Fix the AES key
        fixed_aes = aes_key.encode('utf-8')[:32].decode('utf-8', 'ignore')
        print(f"Fixed AES_KEY: {fixed_aes}")
        print(f"Fixed length: {len(fixed_aes.encode('utf-8'))} bytes")

if __name__ == "__main__":
    generate_all_keys()
    verify_key_lengths()