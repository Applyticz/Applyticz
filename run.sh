#!/bin/bash

# Change to the backend directory
cd backend || { echo "Failed to change directory to backend. Exiting..."; exit 1; }

# Determine Python executable (supports both Python 3.11 or fallback to python3/python)
if command -v python3.11 &>/dev/null; then
    PYTHON_EXEC=python3.11
    echo "Python 3.11 is available."
elif command -v python3 &>/dev/null; then
    PYTHON_EXEC=python3
    echo "Using default Python 3."
elif command -v python &>/dev/null; then
    PYTHON_EXEC=python
    echo "Using default Python."
else
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
    echo "Creating a virtual environment..."
    $PYTHON_EXEC -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment based on the OS
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    echo "Activating the virtual environment for Linux/macOS..."
    source .venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Activating the virtual environment for Windows..."
    source .venv/Scripts/activate
else
    echo "Unknown OS. Cannot activate the virtual environment."
    exit 1
fi

# Upgrade pip, setuptools, and wheel separately
echo "Upgrading pip..."
$PYTHON_EXEC -m pip install --upgrade pip

echo "Upgrading setuptools and wheel..."
pip install --upgrade setuptools wheel

# Install required packages from requirements.txt with verbose output
if [[ -f requirements.txt ]]; then
    echo "Installing required packages..."
    pip install --no-cache-dir -r requirements.txt -v
else
    echo "requirements.txt not found. Skipping package installation."
fi

# Download the spaCy model
echo "Installing spaCy model 'en_core_web_sm'..."
$PYTHON_EXEC -m spacy download en_core_web_sm

echo "Virtual environment activated, using Python 3.11 where available, and required packages installed."



# Ask the user if they want to use Docker and Docker Compose
echo -n "Do you want to use Docker (y/n): "
read -r USE_DOCKER

if [[ "$USE_DOCKER" =~ ^[Yy]$ ]]; then

    echo "Running Docker..."

    # Ask if user wants to recreate Docker Images
    echo -n "Do you want to recreate Docker Images (y/n): "
    read -r RECREATE_DOCKER

    if [[ "$RECREATE_DOCKER" =~ ^[Yy]$ ]]; then
        echo "Recreating Docker Images..."
        docker compose down
        docker compose build  # Rebuild the images
        docker compose up -d
    else
        docker compose up -d
    fi

    # Open backend and frontend in the browser
    echo "Opening backend (http://localhost:8000) and frontend (http://localhost:3000) in the browser..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "http://localhost:8000"
        xdg-open "http://localhost:3000"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:8000"
        open "http://localhost:3000"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        start "http://localhost:8000"
        start "http://localhost:3000"
    fi
else
    echo "Skipping Docker setup. Starting the backend server directly..."

    # Check if port 8000 is in use for backend
    BACKEND_PORT=8000
    if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        PID=$(netstat -ano | findstr :$BACKEND_PORT | findstr LISTEN | awk '{print $5}')
    else
        PID=$(lsof -ti tcp:$BACKEND_PORT)
    fi

    if [ ! -z "$PID" ]; then
        echo "Port $BACKEND_PORT is in use by process $PID. Terminating the process..."
        kill -9 $PID  # Kill the process using the port
        echo "Process $PID terminated. Proceeding to start the backend."
    else
        echo "Port $BACKEND_PORT is free. Starting the backend."
    fi

    # Start the backend server directly on port 8000
    uvicorn app.main:app --reload --host localhost --port 8000 &
        
    # Change to the frontend directory
    cd ../Frontend/app

    # Install dependencies if they haven't been installed yet or if new ones have been added
    echo "Ensuring dependencies are up-to-date..."
    npm install

    # Start the Vite development server
    echo "Starting the React/Vite development server..."
    npm start & 

    # Check if port 3000 is in use for frontend
    FRONTEND_PORT=3000
    if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        PID=$(netstat -ano | findstr :$FRONTEND_PORT | findstr LISTEN | awk '{print $5}')
    else
        PID=$(lsof -ti tcp:$FRONTEND_PORT)
    fi

    if [ ! -z "$PID" ]; then
        echo "Port $FRONTEND_PORT is in use by process $PID. Terminating the process..."
        kill -9 $PID  # Kill the process using the port
        echo "Process $PID terminated. Proceeding to start the frontend."
    else
        echo "Port $FRONTEND_PORT is free. Starting the frontend."
    fi

    # Open backend and frontend in the browser
    echo "Opening backend (http://localhost:8000) and frontend (http://localhost:3000) in the browser..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "http://localhost:8000"
        xdg-open "http://localhost:3000"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:8000"
        open "http://localhost:3000"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        start "http://localhost:8000"
        start "http://localhost:3000"
    fi
fi
