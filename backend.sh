#!/bin/bash

# Change to the backend directory
cd backend  # Ensure the directory name matches (case-sensitive)

# Check if Python 3 or Python is available and use the correct one
if command -v python3 &>/dev/null; then
    PYTHON_EXEC=python3
    PIP_EXEC=pip3
    echo "Python 3 is available."
elif command -v python &>/dev/null; then
    PYTHON_EXEC=python
    PIP_EXEC=pip
    echo "Python is available."
else
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
    echo "Creating a virtual environment..."
    $PYTHON_EXEC -m venv .venv
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source .venv/bin/activate

# Install required packages from requirements.txt
echo "Installing required packages..."
$PIP_EXEC install -r requirements.txt

# Run the FastAPI application
echo "Running the FastAPI application..."
uvicorn app.main:app --reload
