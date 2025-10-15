# install.sh
#!/bin/bash

echo "🔧 Installing RBI NBFC Chatbot..."

# Create virtual environment
python3 -m venv rbi_chatbot_env

# Activate virtual environment
source rbi_chatbot_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create directories
mkdir -p data/raw data/processed data/vector_store src

echo "✅ Installation complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Activate virtual environment: source rbi_chatbot_env/bin/activate"
echo "2. Create .env file with your Google Gemini API key"
echo "3. Run: python main.py --setup"
echo "4. Then test with: python main.py --question \"Your question here\""