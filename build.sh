#!/bin/bash

DOCKER_IMAGE_NAME="abc7223/myfilehub"

echo "Building Docker image..."
docker build -t $DOCKER_IMAGE_NAME .

echo "Pushing Docker image to Docker Hub..."
docker push $DOCKER_IMAGE_NAME

echo "Deployment completed."