#!/usr/bin/env python3
"""
Simple test script
"""
from deploy import SimpleStorage

def main():
    print("🧪 Testing Simple Storage Contract")
    storage = SimpleStorage()
    address, abi = storage.deploy()
    storage.test_contract(address, abi)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main()
