#!/usr/bin/env python3
"""
Simple script to verify the setup is working correctly
"""

def verify_setup():
    print("Verifying web scraping project setup...")
    
    # Test 1: Check Python version
    import sys
    print(f"✓ Python version: {sys.version}")
    
    # Test 2: Check imports
    try:
        import requests
        print("✓ requests imported")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
        
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup imported")
    except ImportError as e:
        print(f"✗ BeautifulSoup import failed: {e}")
        return False
        
    try:
        import pandas as pd
        print("✓ pandas imported")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    # Test 3: Check project structure
    import os
    required_files = ['requirements.txt', 'main.py', 'src/scraper.py', 'src/data_processor.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    # Test 4: Basic functionality test
    try:
        # Test BeautifulSoup
        html = "<div class='test'>Hello World</div>"
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', class_='test').text
        assert result == "Hello World"
        print("✓ BeautifulSoup basic parsing works")
        
        # Test pandas
        data = [{'test': 'data'}]
        df = pd.DataFrame(data)
        assert len(df) == 1
        print("✓ pandas basic functionality works")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    
    print("\n🎉 All setup verification tests passed!")
    print("You can now run: python main.py --website books --output csv")
    return True

if __name__ == "__main__":
    verify_setup()