#!/usr/bin/env python3
"""
Simple test for the working contract
"""
from working_deploy import WorkingSimpleStorage

def main():
    print("🧪 Testing Simple Storage Contract")
    print("=" * 50)
    
    try:
        deployer = WorkingSimpleStorage()
        print("1. Deploying contract...")
        address, abi = deployer.deploy_contract()
        
        print("2. Testing basic functionality...")
        deployer.test_contract_functions(address, abi)
        
        print("\n🎉 ALL TESTS PASSED! Your contract is working perfectly!")
        print(f"📍 Contract: {address}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()