#!/bin/bash

# Mechanical Drawing App - Setup Script for macOS/Linux
echo "🔧 Setting up Mechanical Drawing Application..."

# Check if Python 3.9 is available
if command -v python3.9 &> /dev/null; then
    PYTHON_CMD="python3.9"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Error: Python 3 not found. Please install Python 3.9 or later."
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv mechanical_env

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source mechanical_env/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create outputs directory
mkdir -p outputs

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  source mechanical_env/bin/activate"
echo "  python run_app.py"
echo ""
echo "Or use: ./run_app.sh"