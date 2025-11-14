import pytest
import json
from web3 import Web3
from solcx import compile_standard, install_solc

@pytest.fixture
def setup_contract():
    """Setup the contract for testing"""
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    
    # Compile contract
    install_solc('0.8.0')
    
    with open("./contracts/SimpleStorage.sol", "r") as file:
        simple_storage_file = file.read()
    
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )
    
    # Get bytecode and ABI
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
    
    # Deploy contract
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Use default Ganache account
    account = w3.eth.accounts[0]
    
    transaction = SimpleStorage.constructor().build_transaction({
        "chainId": 1337,
        "from": account,
        "nonce": w3.eth.get_transaction_count(account)
    })
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key="0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Return contract instance
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

def test_initial_value(setup_contract):
    """Test that initial value is 0"""
    contract = setup_contract
    initial_value = contract.functions.getValue().call()
    assert initial_value == 0

def test_increment(setup_contract):
    """Test increment function"""
    contract = setup_contract
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    account = w3.eth.accounts[0]
    
    # Increment
    transaction = contract.functions.increment().build_transaction({
        "from": account,
        "nonce": w3.eth.get_transaction_count(account)
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key="0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Check value
    new_value = contract.functions.getValue().call()
    assert new_value == 1

def test_decrement(setup_contract):
    """Test decrement function"""
    contract = setup_contract
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    account = w3.eth.accounts[0]
    
    # First increment to 1
    transaction = contract.functions.increment().build_transaction({
        "from": account,
        "nonce": w3.eth.get_transaction_count(account)
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key="0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Then decrement
    transaction = contract.functions.decrement().build_transaction({
        "from": account,
        "nonce": w3.eth.get_transaction_count(account)
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key="0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Check value
    new_value = contract.functions.getValue().call()
    assert new_value == 0

if __name__ == "__main__":
    pytest.main([__file__])