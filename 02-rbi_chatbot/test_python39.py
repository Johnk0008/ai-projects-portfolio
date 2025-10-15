# test_python39.py
import sys
print(f"Python version: {sys.version}")

try:
    import google.generativeai as genai
    print("✅ google-generativeai imported successfully")
    print(f"Version: {genai.__version__}")
except ImportError as e:
    print(f"❌ Error: {e}")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
except ImportError as e:
    print(f"❌ Error: {e}")

# Test basic functionality
import os
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_actual_gemini_api_key_here":
    print("✅ API key found and valid")
else:
    print("❌ Please set your API key in .env file")