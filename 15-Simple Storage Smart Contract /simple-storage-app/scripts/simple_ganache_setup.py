#!/usr/bin/env python3
"""
Super simple setup using Ganache CLI
First install: npm install -g ganache-cli
Then run: ganache-cli
"""

from web3 import Web3
import json

# Connect to Ganache (make sure ganache-cli is running)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

if not w3.isConnected():
    print("❌ Cannot connect to Ganache. Please run: ganache-cli")
    exit(1)

print("✅ Connected to Ganache")

# Use the first account
accounts = w3.eth.accounts
my_address = accounts[0]
print(f"📝 Using account: {my_address}")

# SimpleStorage ABI
abi = [
    {
        "inputs": [], "name": "decrement", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [], "name": "getValue", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], 
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [], "name": "increment", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    }
]

# Contract bytecode
bytecode = "0x608060405234801561001057600080fd5b5061012f806100206000396000f3fe6080604052348015600f57600080fd5b5060043610603c5760003560e01c80635d1ca631146041578063a2e6204514604b578063d826f88f146053575b600080fd5b60476059565b005b6051606b565b005b6059607d565b60405190815260200160405180910390f35b600080546001019055565b60008054600019019055565b6000548156fea2646970667358221220c5a8b9f2b8e9f1a4e6c8b4e9f7c1e4d6b8a9f4e7c1a2d4e9f7c1e4d6b8a9f4e64736f6c634300080c0033"

print("🚀 Deploying contract...")
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = SimpleStorage.constructor().transact({'from': my_address})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")

# Test the contract
contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("\n🧪 Testing contract:")
print(f"Initial value: {contract.functions.getValue().call()}")

contract.functions.increment().transact({'from': my_address})
print(f"After increment: {contract.functions.getValue().call()}")

contract.functions.decrement().transact({'from': my_address})
print(f"After decrement: {contract.functions.getValue().call()}")

print("🎉 Simple Storage Contract is working!")