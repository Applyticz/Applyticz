#!/bin/bash

IMAGE_NAME="applyticz-docker"
TAG="latest"
CONTAINER_NAME="applyticz-container"

# Function to check if the image exists locally
image_exists() {
    if [[ "$(docker images -q "$IMAGE_NAME:$TAG" 2> /dev/null)" == "" ]]; then
        return 1  # Image does not exist
    else
        return 0  # Image exists
    fi
}

# Function to check if the container exists
container_exists() {
    docker ps -a --format '{{.Names}}' | grep -w "$CONTAINER_NAME" > /dev/null 2>&1
    return $?
}

# Check if the Docker image already exists
if image_exists; then
    echo "Docker image '$IMAGE_NAME:$TAG' already exists."
else
    echo "Docker image '$IMAGE_NAME:$TAG' not found, building image."
    docker build -t "$IMAGE_NAME:$TAG" .
    if [ $? -ne 0 ]; then
        echo "Error: Failed to build the Docker image."
        exit 1
    fi
fi

# Check if the Docker container already exists
if container_exists; then
    echo "Docker container '$CONTAINER_NAME' already exists."
    
    # If the container exists but is not running, start it
    if [ "$(docker ps -a -f "name=$CONTAINER_NAME" -q)" ] && [ -z "$(docker ps -q -f "name=$CONTAINER_NAME")" ]; then
        echo "Starting existing container."
        docker start "$CONTAINER_NAME"
    else
        echo "Container is already running."
    fi
else
    echo "Running Docker container"
    docker run -d --name "$CONTAINER_NAME" -p 80:80 "$IMAGE_NAME:$TAG"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run the Docker container."
        exit 1
    fi
fi

# Wait for the container to start
sleep 5

# Open localhost/docs in the default browser
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost/docs
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost/docs
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    start http://localhost/docs
else
    echo "Cannot automatically open the browser on this OS. Please visit http://localhost/docs manually."
fi
