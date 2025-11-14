import sys
import os
import json

def check_solcx():
    """Check if solcx is available and working"""
    try:
        from solcx import get_installable_solc_versions, get_solc_version
        print("✅ solcx is available")
        
        # Try to get current version
        try:
            version = get_solc_version()
            print(f"✅ Solidity compiler version: {version}")
            return True
        except:
            print("❌ No Solidity compiler installed")
            return False
            
    except ImportError:
        print("❌ solcx is not installed")
        return False

def install_solc_simple():
    """Simple Solidity compiler installation"""
    try:
        from solcx import install_solc, set_solc_version
        
        print("Installing Solidity compiler...")
        install_solc('0.8.0')
        set_solc_version('0.8.0')
        print("✅ Solidity compiler installed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install Solidity compiler: {e}")
        return False

def compile_contract():
    """Compile the contract with simple error handling"""
    print("🔨 Compiling PollingContract.sol...")
    
    # First, check if solcx is working
    if not check_solcx():
        print("Attempting to install Solidity compiler...")
        if not install_solc_simple():
            print("❌ Cannot compile without Solidity compiler")
            return False
    
    try:
        from solcx import compile_standard
        
        # Read Solidity source code
        with open('PollingContract.sol', 'r') as file:
            source_code = file.read()
        
        print("✅ Source code loaded")
        
        # Simple compilation
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                "PollingContract.sol": {
                    "content": source_code
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "evm.bytecode"]
                    }
                }
            }
        })
        
        # Save compiled data
        with open('PollingContract.json', 'w') as f:
            json.dump(compiled_sol, f, indent=2)
        
        print("✅ Contract compiled successfully")
        print("✅ Compiled data saved to PollingContract.json")
        
        # Show basic info
        contract_data = compiled_sol['contracts']['PollingContract.sol']['PollingSystem']
        abi = contract_data['abi']
        
        print(f"📋 Contract has {len(abi)} ABI entries")
        print("📋 Available functions:")
        for item in abi:
            if item['type'] == 'function':
                inputs = ', '.join([f"{inp['type']} {inp['name']}" for inp in item.get('inputs', [])])
                print(f"   - {item['name']}({inputs})")
        
        return True
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure PollingContract.sol exists in the same directory")
        print("2. Check the Solidity code for syntax errors")
        print("3. Try running: python install_solidity_fixed.py")
        return False

if __name__ == "__main__":
    if compile_contract():
        print("\n🎉 Compilation successful! Next: python run_polling_demo.py")
    else:
        print("\n💥 Compilation failed!")
        sys.exit(1)