#!/usr/bin/env python3
"""
Setup script to install dependencies and compile the contract
"""
import subprocess
import sys
import os

def run_command(command, description):
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    print("🚀 Setting up Simple Storage Contract Environment")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs("contracts", exist_ok=True)
    os.makedirs("scripts", exist_ok=True)
    os.makedirs("tests", exist_ok=True)
    
    # Create the Solidity contract file
    print("📝 Creating SimpleStorage.sol...")
    contract_code = '''// SPDX-License-Identifier: MIT
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
}'''
    
    with open("contracts/SimpleStorage.sol", "w") as f:
        f.write(contract_code)
    print("✅ SimpleStorage.sol created")
    
    print("\n🎉 Setup completed! Now run:")
    print("1. python scripts/working_deploy.py")
    print("2. python scripts/working_interact.py")

if __name__ == "__main__":
    main()