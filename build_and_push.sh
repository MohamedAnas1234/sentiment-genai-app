#!/bin/bash

# Exit on any error
set -e

echo "Sentiment Analysis & GenAI Docker Build Script"
echo "----------------------------------------------"

# Define the image name and tag
DOCKER_USERNAME="anasnasu26"
IMAGE_NAME="sentiment-genai-app"
TAG="latest"
FULL_IMAGE_NAME="$DOCKER_USERNAME/$IMAGE_NAME:$TAG"

echo "Building Docker image: $FULL_IMAGE_NAME"
docker build -t $FULL_IMAGE_NAME .

echo "Build successful. To push, make sure you are logged in using 'docker login'."
read -p "Do you want to push the image to DockerHub now? (y/n): " PUSH_CHOICE

if [ "$PUSH_CHOICE" == "y" ] || [ "$PUSH_CHOICE" == "Y" ]; then
    echo "Pushing image to DockerHub..."
    docker push $FULL_IMAGE_NAME
    echo "Push complete!"
else
    echo "Skipping push."
fi

echo "To run the container locally, use:"
echo "docker run -p 5000:5000 -e GROQ_API_KEY='your_api_key_here' $FULL_IMAGE_NAME"
