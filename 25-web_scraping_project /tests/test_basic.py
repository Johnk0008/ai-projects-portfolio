import unittest
import sys
import os

# Add the parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicSetup(unittest.TestCase):
    
    def test_imports(self):
        """Test basic imports work"""
        try:
            import requests
            from bs4 import BeautifulSoup
            import pandas as pd
            success = True
        except ImportError as e:
            success = False
            print(f"Import error: {e}")
        
        self.assertTrue(success, "All imports should work")
    
    def test_requests(self):
        """Test requests module works with better error handling"""
        import requests
        try:
            # Use a more reliable test endpoint
            response = requests.get('https://httpbin.org/get', timeout=10)
            # Accept any 2xx status code, not just 200
            self.assertTrue(200 <= response.status_code < 300, 
                          f"Expected 2xx status, got {response.status_code}")
        except requests.exceptions.RequestException as e:
            # If there's a network issue, skip the test but don't fail
            self.skipTest(f"Network request failed: {e}")

if __name__ == '__main__':
    unittest.main()