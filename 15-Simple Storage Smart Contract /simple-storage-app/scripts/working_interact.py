import json
from web3 import Web3
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

class WorkingSimpleStorageInteractor:
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
            
            with open("contract_abi.json", "r") as file:
                abi = json.load(file)
            
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            print(f"✅ Loaded contract at: {contract_address}")
            return contract_address, contract
            
        except FileNotFoundError:
            print("❌ No deployed contract found. Please run working_deploy.py first.")
            return None, None
    
    def get_value(self):
        """Read current value"""
        if not self.contract:
            return
        
        try:
            value = self.contract.functions.getValue().call()
            print(f"📊 Current value: {value}")
            return value
        except Exception as e:
            print(f"❌ Error reading value: {e}")
    
    def increment(self):
        """Increment value by 1"""
        if not self.contract:
            return
        
        try:
            print("⏳ Incrementing value...")
            tx_hash = self.contract.functions.increment().transact({
                'from': self.my_address,
                'gas': 100000
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print("✅ Value incremented successfully!")
            print(f"   Transaction: {receipt.transactionHash.hex()}")
            self.get_value()
        except Exception as e:
            print(f"❌ Error incrementing: {e}")
    
    def decrement(self):
        """Decrement value by 1"""
        if not self.contract:
            return
        
        try:
            current_value = self.get_value()
            if current_value == 0:
                print("❌ Cannot decrement: value is already 0")
                return
            
            print("⏳ Decrementing value...")
            tx_hash = self.contract.functions.decrement().transact({
                'from': self.my_address,
                'gas': 100000
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print("✅ Value decremented successfully!")
            print(f"   Transaction: {receipt.transactionHash.hex()}")
            self.get_value()
        except Exception as e:
            print(f"❌ Error decrementing: {e}")
    
    def set_specific_value(self, target_value):
        """Set value to specific number"""
        if not self.contract:
            return
        
        current_value = self.get_value()
        
        if target_value == current_value:
            print(f"📊 Value is already {target_value}")
            return
        
        print(f"🔄 Setting value from {current_value} to {target_value}...")
        
        if target_value > current_value:
            # Need to increment
            increments_needed = target_value - current_value
            for i in range(increments_needed):
                self.contract.functions.increment().transact({
                    'from': self.my_address,
                    'gas': 100000
                })
                print(f"   ➕ Increment {i+1}/{increments_needed}")
        else:
            # Need to decrement
            decrements_needed = current_value - target_value
            for i in range(decrements_needed):
                self.contract.functions.decrement().transact({
                    'from': self.my_address,
                    'gas': 100000
                })
                print(f"   ➖ Decrement {i+1}/{decrements_needed}")
        
        final_value = self.get_value()
        print(f"✅ Value set to {final_value}")
    
    def show_info(self):
        """Show contract and account info"""
        if not self.contract:
            return
        
        print("\n📋 Contract Information:")
        print(f"   Address: {self.contract_address}")
        print(f"   Your account: {self.my_address}")
        print(f"   Balance: {self.w3.eth.get_balance(self.my_address)} wei")
        self.get_value()

def main():
    print("=" * 50)
    print("🤖 Simple Storage Contract Interface")
    print("=" * 50)
    
    interactor = WorkingSimpleStorageInteractor()
    
    if not interactor.contract:
        return
    
    while True:
        print("\n" + "=" * 40)
        print("MENU OPTIONS:")
        print("1. 📊 Get Current Value")
        print("2. ➕ Increment Value")
        print("3. ➖ Decrement Value")
        print("4. 🎯 Set Specific Value")
        print("5. 📋 Show Info")
        print("6. 🚪 Exit")
        print("=" * 40)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            interactor.get_value()
        elif choice == "2":
            interactor.increment()
        elif choice == "3":
            interactor.decrement()
        elif choice == "4":
            try:
                target = int(input("Enter target value: "))
                interactor.set_specific_value(target)
            except ValueError:
                print("❌ Please enter a valid number")
        elif choice == "5":
            interactor.show_info()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()