#!/bin/bash

# Run Script for Mechanical Drawing Application

# Check if virtual environment exists
if [ ! -d "mechanical_env" ]; then
    echo "❌ Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source mechanical_env/bin/activate

# Run the application
echo "🎨 Generating mechanical drawing..."
python run_app.py

# Deactivate virtual environment
deactivate
echo "✅ Done!"