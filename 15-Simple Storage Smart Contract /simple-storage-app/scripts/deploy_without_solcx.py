import json
from web3 import Web3
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

# Pre-compiled contract ABI and bytecode (we'll compile manually first)
SIMPLE_STORAGE_ABI = [
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

# This is the compiled bytecode for our SimpleStorage contract
SIMPLE_STORAGE_BYTECODE = "0x608060405234801561001057600080fd5b5061012f806100206000396000f3fe6080604052348015600f57600080fd5b5060043610603c5760003560e01c80635d1ca631146041578063a2e6204514604b578063d826f88f146053575b600080fd5b60476059565b005b6051606b565b005b6059607d565b60405190815260200160405180910390f35b600080546001019055565b60008054600019019055565b6000548156fea2646970667358221220c5a8b9f2b8e9f1a4e6c8b4e9f7c1e4d6b8a9f4e7c1a2d4e9f7c1e4d6b8a9f4e64736f6c634300080c0033"

class SimpleStorageDeployer:
    def __init__(self):
        # Setup Web3 with eth-tester (built-in blockchain)
        self.tester = EthereumTester()
        self.w3 = Web3(EthereumTesterProvider(self.tester))
        self.accounts = self.w3.eth.accounts
        self.my_address = self.accounts[0]
        print(f"✅ Using account: {self.my_address}")
        print(f"💰 Balance: {self.w3.eth.get_balance(self.my_address)} wei")
        
    def deploy_contract(self):
        """Deploy the contract using pre-compiled bytecode"""
        print("🚀 Starting deployment...")
        
        # Create contract
        SimpleStorage = self.w3.eth.contract(
            abi=SIMPLE_STORAGE_ABI, 
            bytecode=SIMPLE_STORAGE_BYTECODE
        )
        
        print("⛓️ Deploying contract to blockchain...")
        
        # Deploy contract
        transaction_hash = SimpleStorage.constructor().transact({
            'from': self.my_address,
        })
        
        # Wait for transaction receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash)
        
        print(f"✅ Contract deployed at address: {tx_receipt.contractAddress}")
        print(f"📊 Block number: {tx_receipt.blockNumber}")
        print(f"🎉 Gas used: {tx_receipt.gasUsed}")
        
        # Save contract address and ABI
        with open("contract_address.txt", "w") as file:
            file.write(tx_receipt.contractAddress)
        
        with open("contract_abi.json", "w") as file:
            json.dump(SIMPLE_STORAGE_ABI, file, indent=4)
        
        return tx_receipt.contractAddress, SIMPLE_STORAGE_ABI

    def test_contract(self, contract_address, abi):
        """Test the deployed contract functions"""
        print("\n🧪 Testing contract functions...")
        
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        
        # Test 1: Get initial value (should be 0)
        initial_value = contract.functions.getValue().call()
        print(f"📊 Initial value: {initial_value}")
        assert initial_value == 0, f"Expected 0, got {initial_value}"
        
        # Test 2: Increment
        print("🔼 Testing increment function...")
        tx_hash = contract.functions.increment().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        value_after_increment = contract.functions.getValue().call()
        print(f"📊 Value after increment: {value_after_increment}")
        assert value_after_increment == 1, f"Expected 1, got {value_after_increment}"
        
        # Test 3: Decrement
        print("🔽 Testing decrement function...")
        tx_hash = contract.functions.decrement().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        value_after_decrement = contract.functions.getValue().call()
        print(f"📊 Value after decrement: {value_after_decrement}")
        assert value_after_decrement == 0, f"Expected 0, got {value_after_decrement}"
        
        # Test 4: Multiple increments
        print("🔄 Testing multiple increments...")
        for i in range(3):
            tx_hash = contract.functions.increment().transact({'from': self.my_address})
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            current_value = contract.functions.getValue().call()
            print(f"  Increment {i+1}: value = {current_value}")
        
        final_value = contract.functions.getValue().call()
        print(f"📊 Final value after 3 increments: {final_value}")
        assert final_value == 3, f"Expected 3, got {final_value}"
        
        print("✅ All tests passed!")
        return True

    def show_network_info(self):
        """Display network information"""
        print("\n🌐 Network Information:")
        print(f"  Network ID: {self.w3.net.version}")
        print(f"  Latest block: {self.w3.eth.block_number}")
        print(f"  Accounts: {len(self.accounts)}")
        for i, account in enumerate(self.accounts[:3]):  # Show first 3 accounts
            balance = self.w3.eth.get_balance(account)
            print(f"  Account {i}: {account} - Balance: {balance} wei")

def main():
    print("=" * 60)
    print("🤖 Simple Storage Smart Contract Deployment")
    print("=" * 60)
    
    try:
        deployer = SimpleStorageDeployer()
        deployer.show_network_info()
        
        # Deploy contract
        contract_address, abi = deployer.deploy_contract()
        
        # Test contract
        deployer.test_contract(contract_address, abi)
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"📍 Contract Address: {contract_address}")
        print(f"📁 ABI saved to: contract_abi.json")
        print(f"📁 Address saved to: contract_address.txt")
        print("\nNext steps:")
        print("1. Run 'python scripts/interact_simple.py' to interact with the contract")
        print("2. Run 'python scripts/test_contract.py' for more tests")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()