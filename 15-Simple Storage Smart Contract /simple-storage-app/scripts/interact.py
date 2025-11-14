import json
from web3 import Web3
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

class SimpleStorageInteractor:
    def __init__(self):
        # Setup
        self.tester = EthereumTester()
        self.w3 = Web3(EthereumTesterProvider(self.tester))
        self.accounts = self.w3.eth.accounts
        self.my_address = self.accounts[0]
        
        # Load contract
        self.contract = self.load_contract()
    
    def load_contract(self):
        """Load the deployed contract"""
        try:
            with open("contract_address.txt", "r") as f:
                address = f.read().strip()
            
            with open("contract_abi.json", "r") as f:
                abi = json.load(f)
            
            contract = self.w3.eth.contract(address=address, abi=abi)
            print(f"✅ Loaded contract: {address}")
            return contract
            
        except FileNotFoundError:
            print("❌ Contract not found. Please run deploy.py first.")
            return None
    
    def get_value(self):
        """Get current value"""
        if not self.contract:
            return
        
        value = self.contract.functions.getValue().call()
        print(f"📊 Current value: {value}")
        return value
    
    def increment(self):
        """Increment value"""
        if not self.contract:
            return
        
        print("➕ Incrementing...")
        tx_hash = self.contract.functions.increment().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print("✅ Incremented successfully!")
        self.get_value()
    
    def decrement(self):
        """Decrement value"""
        if not self.contract:
            return
        
        current = self.get_value()
        if current == 0:
            print("❌ Cannot decrement: value is 0")
            return
        
        print("➖ Decrementing...")
        tx_hash = self.contract.functions.decrement().transact({'from': self.my_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print("✅ Decremented successfully!")
        self.get_value()

def main():
    print("=" * 40)
    print("🤖 Simple Storage Interface")
    print("=" * 40)
    
    interactor = SimpleStorageInteractor()
    
    if not interactor.contract:
        return
    
    while True:
        print("\nOptions:")
        print("1. 📊 Get Value")
        print("2. ➕ Increment")
        print("3. ➖ Decrement")
        print("4. 🚪 Exit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            interactor.get_value()
        elif choice == "2":
            interactor.increment()
        elif choice == "3":
            interactor.decrement()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
