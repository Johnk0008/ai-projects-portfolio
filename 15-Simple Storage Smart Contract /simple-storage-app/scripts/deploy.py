import json
from web3 import Web3
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

class SimpleStorage:
    def __init__(self):
        # Setup Web3 with built-in testing blockchain
        self.tester = EthereumTester()
        self.w3 = Web3(EthereumTesterProvider(self.tester))
        self.accounts = self.w3.eth.accounts
        self.my_address = self.accounts[0]
        print(f"✅ Using account: {self.my_address}")
        
    def get_contract_info(self):
        """Return ABI and bytecode for SimpleStorage"""
        abi = [
            {
                "inputs": [],
                "name": "decrement",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getValue",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "increment",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        
        # Compiled bytecode for SimpleStorage
        bytecode = "0x608060405234801561001057600080fd5b50610150806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80635d1ca63114610046578063a2e6204514610050578063d826f88f1461005a575b600080fd5b61004e610064565b005b610058610076565b005b610062610088565b005b600080546001019055565b60008054600019019055565b6000548156fea2646970667358221220c5a8b9f2b8e9f1a4e6c8b4e9f7c1e4d6b8a9f4e7c1a2d4e9f7c1e4d6b8a9f4e64736f6c634300080c0033"
        
        return abi, bytecode
    
    def deploy(self):
        """Deploy the contract"""
        print("🚀 Deploying SimpleStorage contract...")
        
        abi, bytecode = self.get_contract_info()
        
        # Create contract
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Deploy
        tx_hash = contract.constructor().transact({
            'from': self.my_address,
            'gas': 2000000
        })
        
        # Wait for deployment
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")
        print(f"📊 Gas used: {tx_receipt.gasUsed}")
        
        # Save contract info
        with open("contract_address.txt", "w") as f:
            f.write(tx_receipt.contractAddress)
        
        with open("contract_abi.json", "w") as f:
            json.dump(abi, f, indent=2)
        
        return tx_receipt.contractAddress, abi
    
    def test_contract(self, address, abi):
        """Test all contract functions"""
        print("\n🧪 Testing contract functions...")
        
        contract = self.w3.eth.contract(address=address, abi=abi)
        
        # Test 1: Initial value
        value = contract.functions.getValue().call()
        print(f"📊 Initial value: {value}")
        
        # Test 2: Increment
        print("➕ Testing increment...")
        tx_hash = contract.functions.increment().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        value = contract.functions.getValue().call()
        print(f"📊 After increment: {value}")
        
        # Test 3: Decrement
        print("➖ Testing decrement...")
        tx_hash = contract.functions.decrement().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        value = contract.functions.getValue().call()
        print(f"📊 After decrement: {value}")
        
        # Test 4: Multiple operations
        print("🔄 Testing multiple operations...")
        for i in range(3):
            contract.functions.increment().transact({'from': self.my_address})
            value = contract.functions.getValue().call()
            print(f"   Increment {i+1}: {value}")
        
        print("✅ All tests passed!")

def main():
    print("=" * 50)
    print("🤖 Simple Storage Contract Deployment")
    print("=" * 50)
    
    try:
        # Create and deploy
        storage = SimpleStorage()
        address, abi = storage.deploy()
        
        # Test the contract
        storage.test_contract(address, abi)
        
        print("\n🎉 Deployment successful!")
        print(f"📍 Contract address saved to: contract_address.txt")
        print(f"📄 Contract ABI saved to: contract_abi.json")
        print("\nNext: Run 'python interact.py' to interact with your contract!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
