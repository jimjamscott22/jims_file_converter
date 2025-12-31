#!/bin/bash
# Quick start script for Jim's File Converter

cd "$(dirname "$0")"

echo "======================================"
echo "🚀 Starting Jim's File Converter"
echo "======================================"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your CloudConvert API key."
    echo "See README.md for setup instructions."
    exit 1
fi

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Warning: Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
    echo "Installing dependencies..."
    .venv/bin/pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Run the application
echo "Starting server..."
.venv/bin/python run.py
