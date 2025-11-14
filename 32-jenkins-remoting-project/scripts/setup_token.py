#!/usr/bin/env python3
"""
Script to help setup and verify Jenkins API token
"""

import os
import getpass
import requests
from urllib.parse import urljoin

def setup_jenkins_token():
    """Interactive script to setup Jenkins API token"""
    
    print("=== Jenkins API Token Setup ===")
    print()
    
    # Get Jenkins URL
    jenkins_url = input("Enter Jenkins URL (e.g., http://localhost:8080): ").strip()
    if not jenkins_url:
        jenkins_url = "http://localhost:8080"
    
    # Get username
    username = input("Enter your Jenkins username: ").strip()
    if not username:
        print("Username is required!")
        return
    
    # Get password/current token
    password = getpass.getpass("Enter your Jenkins password (or current API token): ")
    
    # Test connection with basic auth
    print("\nTesting connection to Jenkins...")
    if test_jenkins_connection(jenkins_url, username, password):
        print("✓ Successfully connected to Jenkins!")
        
        # Instructions for creating new token
        print("\n" + "="*50)
        print("TO CREATE A NEW API TOKEN:")
        print("1. Go to Jenkins in your browser:")
        print(f"   {jenkins_url}")
        print("2. Click your username in top-right corner")
        print("3. Click 'Configure'")
        print("4. Scroll to 'API Token' section")
        print("5. Click 'Add new Token'")
        print("6. Enter token name (e.g., 'python-app')")
        print("7. Click 'Generate'")
        print("8. COPY THE TOKEN IMMEDIATELY (you won't see it again)")
        print("9. Come back here and enter the new token")
        print("="*50)
        
        # Get the new token
        new_token = getpass.getpass("\nPaste your new API token here: ")
        
        # Verify the new token works
        print("\nVerifying new API token...")
        if test_jenkins_connection(jenkins_url, username, new_token):
            print("✓ New API token works successfully!")
            
            # Save to environment file
            save_token_to_env(new_token)
            
            print(f"\n✓ API token has been saved to .env file")
            print("You can now run: python app.py --setup")
        else:
            print("✗ New API token verification failed!")
    
    else:
        print("✗ Failed to connect to Jenkins with provided credentials!")
        print("Please check your URL, username, and password.")

def test_jenkins_connection(jenkins_url: str, username: str, password: str) -> bool:
    """Test connection to Jenkins with provided credentials"""
    try:
        # Test using whoami API
        auth = (username, password)
        response = requests.get(
            urljoin(jenkins_url, '/api/json'),
            auth=auth,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def save_token_to_env(token: str):
    """Save token to .env file"""
    env_content = f"""# Jenkins Configuration
JENKINS_API_TOKEN={token}
JENKINS_URL=http://localhost:8080
JENKINS_USERNAME=admin

# Python Configuration
PYTHONPATH=./src
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Also create a .env.example for reference
    example_content = """# Jenkins Configuration
JENKINS_API_TOKEN=your_jenkins_api_token_here
JENKINS_URL=http://localhost:8080
JENKINS_USERNAME=your_username

# Python Configuration
PYTHONPATH=./src
"""
    
    with open('.env.example', 'w') as f:
        f.write(example_content)

if __name__ == "__main__":
    setup_jenkins_token()