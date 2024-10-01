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
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # For Linux and macOS
    echo "Activating the virtual environment for Linux/macOS..."
    source .venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # For Windows
    echo "Activating the virtual environment for Windows..."
    source .venv/Scripts/activate
else
    echo "Unknown OS. Cannot activate the virtual environment."
    exit 1
fi

# Install required packages from requirements.txt
echo "Installing required packages..."
$PIP_EXEC install -r requirements.txt

# Ask the user if they want to use Docker and Docker Compose
echo -n "Do you want to use Docker (y/n): "
read -r USE_DOCKER

if [[ "$USE_DOCKER" =~ ^[Yy]$ ]]; then
    echo "Running Docker..."
    docker compose up -d

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

    # Check if port 8000 is in use
    PORT=8000
    if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        PID=$(netstat -ano | findstr :$PORT | findstr LISTEN | awk '{print $5}')
    else
        PID=$(lsof -ti tcp:$PORT)
    fi

    if [ ! -z "$PID" ]; then
        echo "Port $PORT is in use by process $PID. Terminating the process..."
        kill -9 $PID  # Kill the process using the port
        echo "Process $PID terminated. Proceeding to start the backend."
    else
        echo "Port $PORT is free. Starting the backend."
    fi

    # Start the backend server directly on port 8000
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
        
    # Change to the frontend directory
    cd ../Frontend/app

    # Install dependencies if they haven't been installed yet or if new ones have been added
    echo "Ensuring dependencies are up-to-date..."
    npm install

    # Start the React development server
    echo "Starting the React development server..."
    npm start &

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
