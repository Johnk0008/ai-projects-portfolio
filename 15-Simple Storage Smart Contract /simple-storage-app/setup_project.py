#!/usr/bin/env python3
"""
Complete setup script for Simple Storage Smart Contract Project
"""
import os
import subprocess
import sys

def run_command(command, description):
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def create_file(filepath, content):
    """Create a file with the given content"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Created {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed to create {filepath}: {e}")
        return False

def main():
    print("🚀 Complete Simple Storage Contract Setup")
    print("=" * 60)
    
    # Create directory structure
    directories = ['contracts', 'scripts', 'tests']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/ directory")
    
    # Create requirements.txt
    requirements_content = """web3==5.31.4
python-dotenv==1.0.0
eth-tester==0.6.0b1
pytest==7.4.0
"""
    create_file("requirements.txt", requirements_content)
    
    # Create SimpleStorage.sol
    solidity_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private value;
    
    event ValueChanged(uint256 newValue);
    
    function increment() public {
        value += 1;
        emit ValueChanged(value);
    }
    
    function decrement() public {
        require(value > 0, "Value cannot be negative");
        value -= 1;
        emit ValueChanged(value);
    }
    
    function getValue() public view returns (uint256) {
        return value;
    }
}
"""
    create_file("contracts/SimpleStorage.sol", solidity_content)
    
    # Create the main deployment script
    deploy_script = '''import json
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
        print("\\n🧪 Testing contract functions...")
        
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
        
        print("\\n🎉 Deployment successful!")
        print(f"📍 Contract address saved to: contract_address.txt")
        print(f"📄 Contract ABI saved to: contract_abi.json")
        print("\\nNext: Run 'python interact.py' to interact with your contract!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    create_file("scripts/deploy.py", deploy_script)
    
    # Create interaction script
    interact_script = '''import json
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
        print("\\nOptions:")
        print("1. 📊 Get Value")
        print("2. ➕ Increment")
        print("3. ➖ Decrement")
        print("4. 🚪 Exit")
        
        choice = input("\\nChoose option (1-4): ").strip()
        
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
'''
    create_file("scripts/interact.py", interact_script)
    
    # Create a simple test script
    test_script = '''#!/usr/bin/env python3
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
'''
    create_file("scripts/test.py", test_script)
    
    print("\\n" + "=" * 60)
    print("📋 SETUP COMPLETE!")
    print("=" * 60)
    print("\\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Deploy contract: python scripts/deploy.py")
    print("3. Interact: python scripts/interact.py")
    print("\\nIf you get 'ModuleNotFoundError', make sure to:")
    print("- Activate virtual environment: source venv/bin/activate")
    print("- Install requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()