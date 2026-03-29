#!/bin/bash
# Quick start script for Jim's File Converter using uv

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

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
    echo "⚠️  Warning: uv is not installed!"
    echo "Install it from: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Run the application
echo "Syncing dependencies with uv..."
uv sync

echo "Starting server..."
uv run python run.py
