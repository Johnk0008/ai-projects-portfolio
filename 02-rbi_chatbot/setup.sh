# setup.sh
#!/bin/bash

echo "Setting up RBI Chatbot Environment..."

# Create virtual environment
python3 -m venv rbi_chatbot_env
source rbi_chatbot_env/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed data/vector_store

echo "Setup complete! Activate virtual environment with:"
echo "source rbi_chatbot_env/bin/activate"