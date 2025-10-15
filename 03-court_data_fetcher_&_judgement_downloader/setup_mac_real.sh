#!/bin/bash

echo "🚀 Setting up Real Court Data Fetcher on macOS..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv court_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source court_env/bin/activate

# Install requirements
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Install wkhtmltopdf for PDF generation
echo "📄 Installing wkhtmltopdf for PDF generation..."
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "Installing wkhtmltopdf via Homebrew..."
    brew install --cask wkhtmltopdf
else
    echo "✓ wkhtmltopdf is already installed"
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p downloads

# Set execute permissions
chmod +x setup_mac_real.sh

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment: source court_env/bin/activate"
echo "2. Run the application: streamlit run court_data_fetcher_real.py"
echo "3. Open your browser and go to: http://localhost:8501"
echo ""
echo "⚖️  Features:"
echo "   - Real eCourts data integration"
echo "   - Case search across High Courts & District Courts"
echo "   - PDF judgment downloads"
echo "   - Daily cause lists"
echo "   - SQLite database storage"