try:
    import matplotlib
    import reportlab
    import pandas
    import numpy
    print("✅ All packages installed successfully!")
    print(f"matplotlib version: {matplotlib.__version__}")
    print(f"numpy version: {numpy.__version__}")
except ImportError as e:
    print(f"❌ Error: {e}")