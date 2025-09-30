#!/bin/bash

# IPO Alert Runner Script for Arch Linux
# This script ensures the correct Python environment is used

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python setup.py"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "⚠️  .env file not found. Please create it from .env.example"
    echo "   cp .env.example .env"
    echo "   nano .env  # Edit with your configuration"
    exit 1
fi

# Run the IPO Alert with the virtual environment Python
echo "🚀 Running IPO Alert..."
"$VENV_PYTHON" "$SCRIPT_DIR/cli.py" "$@"