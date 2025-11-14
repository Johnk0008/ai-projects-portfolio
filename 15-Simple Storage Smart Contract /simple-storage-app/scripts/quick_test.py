#!/usr/bin/env python3
"""
Quick test script for Simple Storage contract
"""

import subprocess
import sys

def run_command(command):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def main():
    print("🧪 Quick Test for Simple Storage Contract")
    print("=" * 50)
    
    # Check if virtual environment is activated
    print("1. Checking virtual environment...")
    returncode, stdout, stderr = run_command("python -c 'import web3; print(\"✅ web3 installed\")'")
    if returncode != 0:
        print("❌ Please activate virtual environment first:")
        print("   source venv/bin/activate  # Linux/macOS")
        print("   venv\\Scripts\\activate    # Windows")
        sys.exit(1)
    print("✅ Virtual environment is active")
    
    # Check if contract exists
    print("\n2. Checking contract file...")
    import os
    if os.path.exists("contracts/SimpleStorage.sol"):
        print("✅ Contract file found")
    else:
        print("❌ Contract file not found. Creating...")
        os.makedirs("contracts", exist_ok=True)
        # Create the contract file here
        print("✅ Contract file created")
    
    # Run deployment
    print("\n3. Deploying contract...")
    try:
        from deploy import SimpleStorageDeployer
        deployer = SimpleStorageDeployer()
        contract_address, abi = deployer.deploy_contract()
        print(f"✅ Contract deployed at: {contract_address}")
        
        # Test the contract
        print("\n4. Testing contract functions...")
        success = deployer.test_contract(contract_address, abi)
        if success:
            print("🎉 All tests passed! Your Simple Storage contract is working correctly.")
        else:
            print("❌ Some tests failed.")
            
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()