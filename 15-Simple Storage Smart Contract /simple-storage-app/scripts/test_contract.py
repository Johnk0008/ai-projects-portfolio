#!/usr/bin/env python3
"""
Test script for Simple Storage contract
"""

from deploy_without_solcx import SimpleStorageDeployer

def run_comprehensive_test():
    print("🧪 Comprehensive Simple Storage Contract Test")
    print("=" * 50)
    
    try:
        # Create deployer instance
        deployer = SimpleStorageDeployer()
        
        # Deploy new contract
        print("1. Deploying contract...")
        contract_address, abi = deployer.deploy_contract()
        
        # Run comprehensive tests
        print("\n2. Running comprehensive tests...")
        contract = deployer.w3.eth.contract(address=contract_address, abi=abi)
        
        # Test initial state
        initial_value = contract.functions.getValue().call()
        assert initial_value == 0, f"Initial value should be 0, got {initial_value}"
        print("✅ Initial value test passed")
        
        # Test multiple increments
        print("\n3. Testing multiple increments...")
        for i in range(5):
            tx_hash = contract.functions.increment().transact({'from': deployer.my_address})
            deployer.w3.eth.wait_for_transaction_receipt(tx_hash)
            current_value = contract.functions.getValue().call()
            assert current_value == i + 1, f"Expected {i + 1}, got {current_value}"
            print(f"  ✅ Increment {i + 1}: value = {current_value}")
        
        # Test multiple decrements
        print("\n4. Testing multiple decrements...")
        for i in range(3):
            tx_hash = contract.functions.decrement().transact({'from': deployer.my_address})
            deployer.w3.eth.wait_for_transaction_receipt(tx_hash)
            current_value = contract.functions.getValue().call()
            expected = 5 - (i + 1)
            assert current_value == expected, f"Expected {expected}, got {current_value}"
            print(f"  ✅ Decrement {i + 1}: value = {current_value}")
        
        # Test final value
        final_value = contract.functions.getValue().call()
        assert final_value == 2, f"Final value should be 2, got {final_value}"
        print(f"✅ Final value test passed: {final_value}")
        
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print(f"📍 Contract Address: {contract_address}")
        print(f"📊 Final Value: {final_value}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)