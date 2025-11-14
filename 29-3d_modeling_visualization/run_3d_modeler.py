#!/usr/bin/env python3
"""
3D Modeling & Visualization Runner
Simple script to run the 3D modeling application
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("📦 Checking dependencies...")
    
    requirements = ['numpy', 'matplotlib']
    
    for package in requirements:
        try:
            __import__(package)
            print(f"   ✅ {package} is installed")
        except ImportError:
            print(f"   ⬇️  Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"   ❌ Failed to install {package}")
                return False
    
    return True

def main():
    """Main function to run the 3D modeler"""
    print("=" * 50)
    print("🚀 3D Modeling & Visualization System")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install required dependencies")
        return 1
    
    print("\n" + "🎯" * 20)
    print("Starting 3D Model Generation...")
    print("🎯" * 20 + "\n")
    
    try:
        # Import and run the main application
        from working_3d_modeler import Simple3DModeler
        
        modeler = Simple3DModeler()
        modeler.generate_all_models()
        
        print("\n" + "🎉" * 20)
        print("SUCCESS! All 3D models generated.")
        print("🎉" * 20)
        
        print("\n📋 Your project deliverables are ready:")
        print("   • 3D Model files (.json & .obj format)")
        print("   • Rendered images (.png format)")
        print("   • Material applications")
        print("   • Professional visualization")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure Python 3.6+ is installed")
        print("   2. Try: pip install numpy matplotlib")
        print("   3. Restart VS Code and try again")
        return 1

if __name__ == "__main__":
    exit_code = main()
    if exit_code == 0:
        print("\n✨ Check the 'output' folder for your 3D models and renders!")
    sys.exit(exit_code)