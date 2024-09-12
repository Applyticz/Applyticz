#!/bin/bash

# Detect the OS
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # For Linux and macOS (use the correct activate path for these platforms)
    source .venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # For Git Bash on Windows or PowerShell (Windows uses Scripts folder)
    source .venv\Scripts\activate
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Install required packages from requirements.txt
pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --reload