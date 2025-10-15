# reinstall.sh
#!/bin/bash

echo "🔧 Reinstalling RBI NBFC Chatbot with clean dependencies..."

# Remove existing virtual environment
if [ -d "rbi_chatbot_env" ]; then
    echo "🗑️ Removing existing virtual environment..."
    rm -rf rbi_chatbot_env
fi

# Create new virtual environment
echo "🐍 Creating new virtual environment..."
python3 -m venv rbi_chatbot_env

# Activate virtual environment
source rbi_chatbot_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install minimal requirements
echo "📦 Installing minimal dependencies..."
pip install langchain==0.0.346
pip install langchain-community==0.0.10
pip install chromadb==0.4.15
pip install pypdf2==3.0.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install google-generativeai==0.3.2

# Create directories
mkdir -p data/raw data/processed data/vector_store src

echo "✅ Clean installation complete!"
echo ""
echo "🚀 Next steps:"
echo "1. source rbi_chatbot_env/bin/activate"
echo "2. Add GOOGLE_API_KEY to .env file"
echo "3. python main.py --setup"
echo "4. python main.py --question \"What are capital requirements?\""