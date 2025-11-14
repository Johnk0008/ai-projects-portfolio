# test_data.py
import pandas as pd

def test_data_loading():
    print("Testing data loading...")
    
    # Test first file
    try:
        df1 = pd.read_csv('data/Unemployment_in_India.csv')
        print(f"✓ File 1 loaded successfully: {df1.shape}")
        print(f"Columns: {list(df1.columns)}")
        print(f"First date values: {df1['Date'].head(3).tolist()}")
    except Exception as e:
        print(f"✗ File 1 failed: {e}")
    
    # Test second file  
    try:
        df2 = pd.read_csv('data/Unemployment_Rate_upto_11_2020.csv')
        print(f"✓ File 2 loaded successfully: {df2.shape}")
        print(f"Columns: {list(df2.columns)}")
        print(f"First date values: {df2['Date'].head(3).tolist()}")
    except Exception as e:
        print(f"✗ File 2 failed: {e}")

if __name__ == "__main__":
    test_data_loading()