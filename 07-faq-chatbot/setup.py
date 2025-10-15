import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return False

def setup_environment():
    print("Setting up FAQ Chatbot Environment...")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv"):
            print("Failed to create virtual environment")
            return False
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:  # macOS/Linux
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Upgrade pip
    print("Upgrading pip...")
    run_command(f'"{python_path}" -m pip install --upgrade pip')
    
    # Install packages
    packages = [
        "flask==2.3.3",
        "nltk==3.8.1", 
        "scikit-learn==1.3.2",
        "numpy==1.24.3",
        "spacy==3.7.2",
        "python-dotenv==1.0.0",
        "thread6==0.2.1"
    ]
    
    print("Installing packages...")
    for package in packages:
        print(f"Installing {package}...")
        if not run_command(f'"{pip_path}" install {package}'):
            print(f"Failed to install {package}")
    
    # Download NLTK data
    print("Downloading NLTK data...")
    nltk_commands = [
        "import nltk; nltk.download('punkt')",
        "import nltk; nltk.download('stopwords')"
    ]
    
    for cmd in nltk_commands:
        run_command(f'"{python_path}" -c "{cmd}"')
    
    # Download spaCy model
    print("Downloading spaCy model...")
    run_command(f'"{python_path}" -m spacy download en_core_web_sm')
    
    print("Setup completed!")
    print("\nTo activate the virtual environment:")
    if os.name == 'nt':
        print("venv\\Scripts\\activate")
    else:
        print("source venv/bin/activate")
    print("\nThen run: python app.py")

if __name__ == "__main__":
    setup_environment()