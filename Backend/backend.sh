#!/bin/bash

# Check if Python 3 or Python is available and use the correct one
if command -v python3 &>/dev/null; then
    PYTHON_EXEC=python3
    echo "Python 3 is available."
elif command -v python &>/dev/null; then
    PYTHON_EXEC=python
    echo "Python is available."
else
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
    $PYTHON_EXEC -m venv .venv
fi

# Detect the OS
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # For Linux and macOS (use the correct activate path for these platforms)
    source .venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # For Git Bash on Windows or PowerShell (Windows uses Scripts folder)
    source .venv/Scripts/activate
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Install required packages from requirements.txt
pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --reload
