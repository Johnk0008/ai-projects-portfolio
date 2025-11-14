import subprocess
import sys

def check_and_install_deps():
    """Check and install only necessary dependencies"""
    print("🔍 Checking and installing dependencies...")
    
    # Only install these core packages
    core_packages = [
        "web3==6.0.0",
        "eth-tester==0.9.0", 
        "python-dotenv==1.0.0"
    ]
    
    for package in core_packages:
        package_name = package.split('==')[0]
        print(f"\n📦 Checking {package_name}...")
        
        try:
            # Try to import the package
            if package_name == "web3":
                import web3
                print(f"✅ {package_name} is already installed")
            elif package_name == "eth-tester":
                import eth_tester
                print(f"✅ {package_name} is already installed")
            elif package_name == "python-dotenv":
                import dotenv
                print(f"✅ {package_name} is already installed")
        except ImportError:
            print(f"❌ {package_name} not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package_name} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package_name}")

def check_solcx():
    """Check if solcx is available"""
    print("\n🔨 Checking Solidity compiler...")
    try:
        from solcx import get_installable_solc_versions
        versions = get_installable_solc_versions()
        print(f"✅ solcx is available")
        print(f"📋 Installable versions: {[str(v) for v in versions[:3]]}")
        return True
    except ImportError:
        print("❌ solcx not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "py-solc-x==2.0.1"])
            print("✅ solcx installed successfully")
            
            # Try to install solc
            from solcx import install_solc
            install_solc('0.8.0')
            print("✅ Solidity compiler installed")
            return True
        except Exception as e:
            print(f"❌ Failed to setup solcx: {e}")
            return False

def main():
    print("🚀 SIMPLE DEPENDENCY CHECK")
    print("=" * 40)
    
    check_and_install_deps()
    check_solcx()
    
    print("\n" + "=" * 40)
    print("✅ Dependency check completed!")
    print("💡 Now run: python clean_polling_system.py")

if __name__ == "__main__":
    main()