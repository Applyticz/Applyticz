#!/bin/bash

# Activate the virtual environment
source ./venv/Scripts/activate

# Install required packages from requirements.txt
pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --reload
