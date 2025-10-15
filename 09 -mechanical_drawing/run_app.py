#!/usr/bin/env python3
"""
Run Script for Mechanical Drawing Application
Enhanced with better Python detection
"""

import subprocess
import sys
import os
import platform

def get_python_command():
    """Get the correct Python command for the system"""
    commands_to_try = ['python', 'python3', 'py']
    
    for cmd in commands_to_try:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Check if it's Python 3
                if 'Python 3' in result.stdout or 'Python 3' in result.stderr:
                    print(f"✅ Found Python: {cmd}")
                    return cmd
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    
    print("❌ No Python 3 installation found.")
    print("Please install Python 3.9 or later from https://python.org")
    return None

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['matplotlib', 'numpy', 'reportlab', 'Pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(python_cmd):
    """Install required packages"""
    print("Installing dependencies...")
    try:
        # Use the correct python command to install packages
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup the environment if needed"""
    if not os.path.exists('mechanical_env'):
        print("Virtual environment not found. Creating...")
        python_cmd = get_python_command()
        if not python_cmd:
            return False
        
        try:
            subprocess.check_call([python_cmd, "-m", "venv", "mechanical_env"])
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    
    return True

def main():
    print("🚀 Mechanical Drawing App - Enhanced Setup")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Running in virtual environment")
        # Check and install dependencies
        missing_packages = check_dependencies()
        if missing_packages:
            if not install_dependencies(sys.executable):
                print("Please install dependencies manually:")
                print("pip install -r requirements.txt")
                return
    else:
        print("⚠️  Not in virtual environment - checking setup...")
        if not setup_environment():
            print("\nPlease run the setup script first:")
            if platform.system() == "Windows":
                print("setup.bat")
            else:
                print("./setup.sh")
            return
        
        # Activate virtual environment and rerun
        print("\nPlease activate the virtual environment and run again:")
        if platform.system() == "Windows":
            print("mechanical_env\\Scripts\\activate.bat")
            print("python run_app.py")
        else:
            print("source mechanical_env/bin/activate")
            print("python run_app.py")
        return
    
    print("\n" + "=" * 50)
    print("Starting Mechanical Drawing Generation...")
    print("=" * 50)
    
    # Run the main application
    try:
        from main import main as app_main
        app_main()
    except Exception as e:
        print(f"Error running application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure virtual environment is activated")
        print("2. Try: pip install -r requirements.txt")
        print("3. Check Python version (requires 3.9+): python --version")

if __name__ == "__main__":
    main()