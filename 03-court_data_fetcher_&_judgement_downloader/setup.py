import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except Exception as e:
        print(f"❌ Error installing packages: {e}")

def create_downloads_folder():
    """Create downloads directory"""
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        print("✅ Created downloads folder")

if __name__ == "__main__":
    install_requirements()
    create_downloads_folder()
    print("\n🎉 Setup completed!")
    print("📝 Next steps:")
    print("1. Install wkhtmltopdf (see instructions above)")
    print("2. Run: streamlit run court_data_fetcher.py")