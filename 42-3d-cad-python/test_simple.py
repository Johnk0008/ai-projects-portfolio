#!/usr/bin/env python3
"""
Simple test to verify basic functionality
"""

try:
    import numpy as np
    print("✓ numpy OK")
    
    import matplotlib.pyplot as plt
    print("✓ matplotlib OK")
    
    import plotly.graph_objects as go
    print("✓ plotly OK")
    
    print("\nAll dependencies working! You can run the CAD generator.")
    
    # Test basic functionality
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.figure(figsize=(8, 4))
    plt.plot(x, y)
    plt.title('Test Plot - Working!')
    plt.savefig('test_plot.png', dpi=100, bbox_inches='tight')
    plt.close()
    
    print("✓ Basic plotting test passed")
    print("✓ Test plot saved as 'test_plot.png'")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure virtual environment is activated")
    print("2. Run: pip install numpy matplotlib plotly")
    print("3. If on macOS, try: pip install --upgrade pip")