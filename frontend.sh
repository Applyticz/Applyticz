#!/bin/bash

# Change to the frontend directory
cd Frontend/app

# Install dependencies if they haven't been installed yet or if new ones have been added
echo "package-lock.json found, ensuring dependencies are up-to-date..."
echo "Installing required packages..."
npm install

# Start the React development server
echo "Starting the React development server..."
npm start
