#!/usr/bin/env python3
"""
Simple test script for Simple Storage contract
"""

from deploy_fixed import SimpleStorageDeployer

def main():
    print("🧪 Simple Storage Contract Test")
    print("=" * 50)
    
    try:
        # Create deployer instance
        deployer = SimpleStorageDeployer()
        
        print("1. Deploying contract...")
        contract_address, abi = deployer.deploy_contract()
        
        print("\n2. Running basic functionality tests...")
        contract = deployer.w3.eth.contract(address=contract_address, abi=abi)
        
        # Test 1: Initial value should be 0
        initial_value = contract.functions.getValue().call()
        print(f"✅ Initial value: {initial_value}")
        
        # Test 2: Increment
        tx_hash = contract.functions.increment().transact({'from': deployer.my_address, 'gas': 100000})
        deployer.w3.eth.wait_for_transaction_receipt(tx_hash)
        value_after_increment = contract.functions.getValue().call()
        print(f"✅ After increment: {value_after_increment}")
        
        # Test 3: Decrement
        tx_hash = contract.functions.decrement().transact({'from': deployer.my_address, 'gas': 100000})
        deployer.w3.eth.wait_for_transaction_receipt(tx_hash)
        value_after_decrement = contract.functions.getValue().call()
        print(f"✅ After decrement: {value_after_decrement}")
        
        # Test 4: Multiple operations
        print("\n3. Testing multiple operations...")
        for i in range(2):
            contract.functions.increment().transact({'from': deployer.my_address, 'gas': 100000})
        final_value = contract.functions.getValue().call()
        print(f"✅ After 2 increments: {final_value}")
        
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"📍 Contract Address: {contract_address}")
        print(f"📊 Final Value: {final_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)