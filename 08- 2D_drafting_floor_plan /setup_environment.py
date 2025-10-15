import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")

# Required packages
packages = [
    "matplotlib",
    "reportlab", 
    "pandas",
    "numpy"
]

print("Installing required packages...")
for package in packages:
    install_package(package)

print("\nVerifying installations...")
try:
    import matplotlib
    import reportlab
    import pandas
    import numpy
    print("✅ All packages verified successfully!")
    print("You can now run the floor plan generator.")
except ImportError as e:
    print(f"❌ Verification failed: {e}")