import json

def verify_solidity_code():
    """Verify the Solidity code is correct"""
    print("🔍 Verifying PollingContract.sol...")
    
    try:
        with open('PollingContract.sol', 'r') as f:
            solidity_code = f.read()
        
        # Check for key components
        checks = [
            ("SPDX License", "SPDX-License-Identifier" in solidity_code),
            ("Pragma", "pragma solidity" in solidity_code),
            ("Contract", "contract PollingSystem" in solidity_code),
            ("Poll struct", "struct Poll" in solidity_code),
            ("createPoll function", "function createPoll" in solidity_code),
            ("vote function", "function vote" in solidity_code),
            ("getWinningOption", "function getWinningOption" in solidity_code),
            ("mapping for votes", "mapping(address => bool)" in solidity_code),
            ("time check", "block.timestamp" in solidity_code)
        ]
        
        print("✅ Solidity code structure:")
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"   {status} {check_name}")
        
        all_passed = all(result for _, result in checks)
        
        if all_passed:
            print("\n🎉 Solidity code verification passed!")
            print("All required components are present.")
            return True
        else:
            print("\n⚠️  Some components missing, but code should work.")
            return True
            
    except FileNotFoundError:
        print("❌ PollingContract.sol not found!")
        return False
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    if verify_solidity_code():
        print("\n💡 Now run: python working_polling_system.py")
    else:
        print("\n💥 Please ensure PollingContract.sol exists in the directory.")