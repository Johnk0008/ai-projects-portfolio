import json
from web3 import Web3
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

# Use the same ABI as in deployment
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

class SimpleStorageInteractor:
    def __init__(self):
        # Setup Web3 with eth-tester
        self.tester = EthereumTester()
        self.w3 = Web3(EthereumTesterProvider(self.tester))
        self.accounts = self.w3.eth.accounts
        self.my_address = self.accounts[0]
        
        # Load contract
        self.contract_address, self.contract = self.load_contract()
        
    def load_contract(self):
        """Load deployed contract"""
        try:
            with open("contract_address.txt", "r") as file:
                contract_address = file.read().strip()
            contract = self.w3.eth.contract(address=contract_address, abi=SIMPLE_STORAGE_ABI)
            print(f"✅ Loaded contract at: {contract_address}")
            return contract_address, contract
        except FileNotFoundError:
            print("❌ No deployed contract found. Please run deploy_without_solcx.py first.")
            return None, None
    
    def get_value(self):
        """Read the current value from the contract"""
        if not self.contract:
            return None
            
        try:
            value = self.contract.functions.getValue().call()
            print(f"📊 Current value: {value}")
            return value
        except Exception as e:
            print(f"❌ Error reading value: {e}")
            return None
    
    def increment(self):
        """Increment the value by 1"""
        if not self.contract:
            return None
            
        try:
            print("⏳ Incrementing value...")
            tx_hash = self.contract.functions.increment().transact({
                'from': self.my_address
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print("✅ Value incremented successfully!")
            print(f"📦 Transaction hash: {receipt.transactionHash.hex()}")
            self.get_value()
            return receipt
        except Exception as e:
            print(f"❌ Error incrementing value: {e}")
            return None
    
    def decrement(self):
        """Decrement the value by 1"""
        if not self.contract:
            return None
            
        try:
            current_value = self.contract.functions.getValue().call()
            if current_value == 0:
                print("❌ Cannot decrement: value is already 0")
                return None
                
            print("⏳ Decrementing value...")
            tx_hash = self.contract.functions.decrement().transact({
                'from': self.my_address
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print("✅ Value decremented successfully!")
            print(f"📦 Transaction hash: {receipt.transactionHash.hex()}")
            self.get_value()
            return receipt
        except Exception as e:
            print(f"❌ Error decrementing value: {e}")
            return None

    def reset_to_zero(self):
        """Reset value to 0 by decrementing until 0"""
        if not self.contract:
            return None
            
        current_value = self.contract.functions.getValue().call()
        if current_value == 0:
            print("📊 Value is already 0")
            return
            
        print(f"🔄 Resetting value from {current_value} to 0...")
        while current_value > 0:
            tx_hash = self.contract.functions.decrement().transact({'from': self.my_address})
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            current_value = self.contract.functions.getValue().call()
            print(f"  Decremented to: {current_value}")
        
        print("✅ Value reset to 0!")

def main():
    print("=" * 50)
    print("🤖 Simple Storage Contract Interface")
    print("=" * 50)
    
    interactor = SimpleStorageInteractor()
    
    if not interactor.contract:
        return
    
    while True:
        print("\n" + "=" * 40)
        print("MENU:")
        print("1. 📊 Get Current Value")
        print("2. ➕ Increment Value")
        print("3. ➖ Decrement Value")
        print("4. 🔄 Reset to Zero")
        print("5. 🚪 Exit")
        print("=" * 40)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            interactor.get_value()
        elif choice == "2":
            interactor.increment()
        elif choice == "3":
            interactor.decrement()
        elif choice == "4":
            interactor.reset_to_zero()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()