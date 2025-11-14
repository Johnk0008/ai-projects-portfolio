import json
import sys

def compile_contract():
    """Simple contract compilation"""
    print("🔨 Compiling PollingContract.sol...")
    
    try:
        from solcx import compile_standard
        
        # Read source code
        with open('PollingContract.sol', 'r') as f:
            source_code = f.read()
        
        # Compile
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
        
        # Save to file
        with open('PollingContract.json', 'w') as f:
            json.dump(compiled_sol, f, indent=2)
        
        print("✅ Contract compiled successfully!")
        
        # Show basic info
        contract_data = compiled_sol['contracts']['PollingContract.sol']['PollingSystem']
        abi = contract_data['abi']
        
        print(f"📋 Contract has {len(abi)} functions and events")
        
        return True
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        return False

if __name__ == "__main__":
    if compile_contract():
        print("\n🎉 Compilation successful! Run: python clean_polling_system.py")
    else:
        print("\n💥 Compilation failed!")
        sys.exit(1)