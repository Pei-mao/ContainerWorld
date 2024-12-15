#!/bin/bash

# Script to start a Docker registry with authentication and TLS
# Author: [Your Name]
# Date: [Optional]
# Usage: Run this script to start a Docker registry using the specified parameters

# Define variables
REGISTRY_NAME="registry"
REGISTRY_IMAGE="registry:2"
HOST_PORT=5002
CONTAINER_PORT=5000
AUTH_DIR="$(pwd)/auth"
CERTS_DIR="$(pwd)/certs"
DATA_DIR="$(pwd)/data"
TLS_CERT="/certs/cert.crt"
TLS_KEY="/certs/cert.key"
REALM="Registry Realm"
HTPASSWD_PATH="/auth/htpasswd"

# Automatically detect the server's IP address
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS 系統使用 ifconfig
  SERVER_IP=$(ifconfig | grep 'en0' -A 3 | grep inet | tail -n1 | awk '{print $2}')
else
  # Linux 系統使用 hostname -I
  SERVER_IP=$(hostname -I | awk '{print $1}')
fi

# Ensure required directories exist
mkdir -p "$AUTH_DIR" "$CERTS_DIR" "$DATA_DIR"

# Run the Docker registry container
docker run -d -p "$HOST_PORT:$CONTAINER_PORT" --name "$REGISTRY_NAME" \
  -v "$AUTH_DIR:/auth" \
  -v "$CERTS_DIR:/certs" \
  -v "$DATA_DIR:/var/lib/registry" \
  -e REGISTRY_HTTP_TLS_CERTIFICATE="$TLS_CERT" \
  -e REGISTRY_HTTP_TLS_KEY="$TLS_KEY" \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="$REALM" \
  -e REGISTRY_AUTH_HTPASSWD_PATH="$HTPASSWD_PATH" \
  "$REGISTRY_IMAGE"

# Check if the Docker container started successfully
if [[ $? -eq 0 ]]; then
  echo "Docker registry started successfully!"
  echo "Access it at https://${SERVER_IP:-localhost}:$HOST_PORT"
else
  echo "Failed to start the Docker registry. Please check the script and Docker configuration."
  exit 1
fi
