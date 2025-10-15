# install_dependencies.sh
#!/bin/bash

echo "Installing RBI Chatbot Dependencies..."

# Create virtual environment if it doesn't exist
if [ ! -d "rbi_chatbot_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv rbi_chatbot_env
fi

# Activate virtual environment
source rbi_chatbot_env/bin/activate

# Install requirements
echo "Installing packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed data/vector_store src

echo "Installation complete!"
echo "To activate the virtual environment: source rbi_chatbot_env/bin/activate"