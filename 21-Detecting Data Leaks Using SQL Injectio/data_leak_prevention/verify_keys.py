#!/usr/bin/env python3
"""
Verify that your keys meet security requirements
"""

import os

def verify_environment():
    """Verify all environment variables are set correctly"""
    print("🔍 Verifying Environment Configuration")
    print("=" * 50)
    
    required_vars = ['SECRET_KEY', 'AES_KEY', 'DATABASE_URL']
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'AES_KEY':
                byte_length = len(value.encode('utf-8'))
                status = "✅" if byte_length == 32 else "❌"
                print(f"{status} {var}: Set ({byte_length} bytes)")
                if byte_length != 32:
                    print(f"   ⚠️  AES key should be exactly 32 bytes")
                    all_good = False
            else:
                print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All environment variables are properly configured!")
    else:
        print("⚠️  Some issues found. Please run the key generator.")
    
    return all_good

if __name__ == "__main__":
    # Load .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    verify_environment()