#!/bin/bash

# Exit on error
set -e

# Check if project ID is provided
if [ -z "$1" ]; then
    echo "Please provide your Google Cloud project ID"
    echo "Usage: ./deploy-gke.sh YOUR_PROJECT_ID"
    exit 1
fi

PROJECT_ID=$1

# Replace project ID in Kubernetes configs
sed -i '' "s/YOUR_PROJECT_ID/$PROJECT_ID/g" k8s/deployment.yaml

# Build and tag Docker images
echo "Building Docker images..."
docker build --target backend -t gcr.io/$PROJECT_ID/quantum-duality-backend:latest .
docker build --target frontend-build -t gcr.io/$PROJECT_ID/quantum-duality-frontend:latest .

# Push images to Google Container Registry
echo "Pushing images to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/quantum-duality-backend:latest
docker push gcr.io/$PROJECT_ID/quantum-duality-frontend:latest

# Create GKE cluster if it doesn't exist
if ! gcloud container clusters describe qdt-cluster --region=us-central1 > /dev/null 2>&1; then
    echo "Creating GKE cluster..."
    gcloud container clusters create qdt-cluster \
        --num-nodes=3 \
        --machine-type=e2-standard-2 \
        --region=us-central1
fi

# Get credentials for kubectl
echo "Getting cluster credentials..."
gcloud container clusters get-credentials qdt-cluster --region=us-central1

# Apply Kubernetes configurations
echo "Applying Kubernetes configurations..."
kubectl apply -f k8s/storage.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for services to be ready
echo "Waiting for services to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/frontend
kubectl wait --for=condition=available --timeout=300s deployment/backend
kubectl wait --for=condition=available --timeout=300s deployment/redis

# Get the external IP
echo "Getting external IP..."
kubectl get service frontend-service

echo "Deployment complete! Your application should be accessible at the external IP above."

# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Google Cloud SDK
brew install --cask google-cloud-sdk

gcloud init

gcloud auth login
gcloud container clusters get-credentials qdt-cluster --region=us-central1 --project=hip-informatics-446103-u3 

gcloud compute addresses list --project hip-informatics-446103-u3 