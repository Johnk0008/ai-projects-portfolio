#!/usr/bin/env python3
"""
Quick fix script to resolve AES key issues
"""

def generate_proper_aes_key():
    """Generate a proper 32-byte AES key"""
    key = "this-is-a-32-byte-key-for-aes-256!"
    if len(key) != 32:
        key = key.ljust(32)[:32]
    print(f"AES Key (32 bytes): {key}")
    print(f"Key length: {len(key)}")
    return key

if __name__ == "__main__":
    generate_proper_aes_key()