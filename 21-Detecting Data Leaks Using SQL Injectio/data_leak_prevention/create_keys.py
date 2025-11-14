#!/usr/bin/env python3
"""
Simple key generator to fix the current issues
"""

import secrets
import string

def generate_proper_keys():
    print("🔐 Generating Proper Security Keys")
    print("=" * 50)
    
    # Generate a proper 32-character secret key
    secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits + '_-') for _ in range(32))
    
    # Generate a proper 32-byte AES key
    aes_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    env_content = f"""SECRET_KEY={secret_key}
AES_KEY={aes_key}
DATABASE_URL=sqlite:///./data_leak_prevention.db
"""
    
    print("✅ Generated Keys:")
    print(env_content)
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Keys saved to .env file")
    print("🔒 Please restart your application")
    
    return secret_key, aes_key

if __name__ == "__main__":
    generate_proper_keys()