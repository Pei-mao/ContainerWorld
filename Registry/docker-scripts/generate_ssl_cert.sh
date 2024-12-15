#!/bin/bash

# Script to generate a self-signed SSL certificate using OpenSSL
# Author: [Your Name]
# Date: [Optional]
# Usage: Run this script to create a self-signed SSL certificate for a specific IP address

# Define variables
CERTS_DIR="certs"
CERT_KEY="${CERTS_DIR}/cert.key"
CERT_CRT="${CERTS_DIR}/cert.crt"
IP="192.168.2.130" # Update this to your desired IP address
DAYS=365           # Certificate validity in days

# Create the certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

# Generate the SSL certificate
openssl req -x509 -newkey rsa:4096 -nodes -keyout "$CERT_KEY" -out "$CERT_CRT" -days "$DAYS" \
  -subj "/CN=$IP" \
  -addext "subjectAltName=IP:$IP"

# Check if the certificate generation was successful
if [[ $? -eq 0 ]]; then
  echo "SSL certificate generated successfully!"
  echo "Key: $CERT_KEY"
  echo "Certificate: $CERT_CRT"
else
  echo "Failed to generate SSL certificate. Please check the script and your OpenSSL configuration."
  exit 1
fi
