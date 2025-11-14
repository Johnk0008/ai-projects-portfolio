#!/usr/bin/env python3
"""
Setup environment for Jenkins Remoting Project
"""

import os
import sys
import subplatform

def setup_environment():
    """Setup the complete environment for Jenkins remoting"""
    
    print("Setting up Jenkins Remoting Environment...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python scripts/setup_token.py")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verify Jenkins connection
    token = os.getenv('JENKINS_API_TOKEN')
    if not token:
        print("❌ JENKINS_API_TOKEN not found in .env file!")
        return False
    
    print("✓ Environment variables loaded")
    
    # Test Jenkins connection
    from src.jenkins_controller import JenkinsController
    try:
        jc = JenkinsController()
        user_info = jc.jenkins.get_whoami()
        print(f"✓ Connected to Jenkins as: {user_info['fullName']}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Jenkins: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'config/node_configs', 'scripts', 'tests']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

if __name__ == "__main__":
    create_directories()
    
    if setup_environment():
        print("\n🎉 Environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python app.py --setup (to create sample nodes)")
        print("2. Run: python app.py --monitor (to start monitoring)")
    else:
        print("\n❌ Environment setup failed!")
        sys.exit(1)