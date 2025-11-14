#!/usr/bin/env python3
"""
Final test to verify all dependencies work
"""

def test_dependencies():
    """Test all required dependencies"""
    try:
        import numpy as np
        print("✅ numpy - OK")
        
        import matplotlib
        print("✅ matplotlib - OK")
        
        import plotly
        print("✅ plotly - OK")
        
        print("\n🎉 All dependencies working!")
        print("You can now run: python new_cad_main.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nTo install dependencies, run:")
        print("pip install numpy matplotlib plotly")
        return False

if __name__ == "__main__":
    test_dependencies()