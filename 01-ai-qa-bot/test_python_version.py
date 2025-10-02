# test_python_version.py
import sys
import pkg_resources

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Check key packages
packages = ['openai', 'streamlit', 'python-dotenv', 'requests']
for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"✅ {package}: {version}")
    except:
        print(f"❌ {package}: Not installed")