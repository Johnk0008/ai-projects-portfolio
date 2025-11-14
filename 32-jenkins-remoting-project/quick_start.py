#!/usr/bin/env python3
import os

# Create environment file
with open('.env', 'w') as f:
    f.write("""JENKINS_API_TOKEN=mock_token
JENKINS_URL=http://localhost:8080
JENKINS_USERNAME=admin
MOCK_MODE=true
""")

print("✅ Configuration created!")
print("Run: python app.py --status")