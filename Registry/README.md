# Configuring Docker to Set Up a Private Registry

## Table of Contents
1. [Introduction](#introduction) 🛠️
2. [Requirements](#requirements) 📋
3. [Setup on macOS](#setup-on-macos) 🍎
4. [Setup on Linux](#setup-on-linux) 🐧
5. [Validation](#validation) ✅

---

## Introduction

📦 This guide explains how to configure Docker to trust a self-signed certificate for a private Docker registry. By following this guide, you will ensure secure communication between Docker clients and your private registry at `https://192.168.2.130:5002`.

---

## Requirements

- **Operating Systems**:
  - `macOS Monterey or later` 🍎
  - `Ubuntu 20.04 or later` 🐧
- **Software**:
  - `Docker 20.10 or later` 🐳
  - `OpenSSL` for generating self-signed certificates 🔐
  - `A browser` for HTTPS testing 🌐

---

## Setup on macOS

### 1. Generate Self-Signed Certificate
On the private registry server, generate a self-signed certificate:
```bash
cd Registry
mkdir -p certs auth data
openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/cert.key -out certs/cert.crt -days 365 \
  -subj "/CN=192.168.2.130" \
  -addext "subjectAltName=IP:192.168.2.130"
```

### 2. Configure the Registry
Start the Docker registry with the generated certificate:
```bash
docker run -d -p 5002:5000 --name registry \
  -v "$(pwd)/auth:/auth" \
  -v "$(pwd)/certs:/certs" \
  -v "$(pwd)/data:/var/lib/registry" \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/cert.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/cert.key \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry:2
```

### 3. Trust the Certificate on macOS
Combine the following steps to trust the self-signed certificate on macOS:
```bash
# Rename the certificate file
mv /Users/username/Desktop/cert.crt /Users/username/Desktop/ca.crt

# Add the certificate to the macOS trust store
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /Users/username/Desktop/ca.crt
```

---

## Setup on Linux

### 1. Generate Self-Signed Certificate and Configure the Registry
Follow the same steps as in macOS to generate the certificate and configure the registry.

### 2. Trust the Certificate on Linux
Combine the following steps to trust the self-signed certificate on Linux:
```bash
# Rename the certificate file
mv /path/to/cert.crt /path/to/ca.crt

# Add the certificate to Docker's trusted directory
sudo mkdir -p /etc/docker/certs.d/192.168.2.130:5002
sudo cp /path/to/ca.crt /etc/docker/certs.d/192.168.2.130:5002/ca.crt

# Restart Docker to apply the changes
sudo systemctl restart docker
```

---

## Validation

### Validate Using a Browser 🌐

Navigate to the following URL in a browser:
```bash
https://192.168.2.130:5002/v2/_catalog
```
Expected JSON response:
```json
{
  "repositories": ["hello-world"]
}
```

### Validate Using Docker 🐳

Combine the following steps to validate the private registry using Docker:
```bash
# Step 1: Log in to the Registry
docker login https://192.168.2.130:5002

# Step 2: Tag a Local Image
docker tag hello-world 192.168.2.130:5002/hello-world

# Step 3: Push the Image
docker push 192.168.2.130:5002/hello-world

# Step 4: Pull the Image
docker pull 192.168.2.130:5002/hello-world
```

### Validate Using curl 📡

Combine the following steps to validate using curl:
```bash
# List All Repositories
curl -u jacky:123456 https://192.168.2.130:5002/v2/_catalog

# Expected output:
# {
#   "repositories": ["hello-world"]
# }

# Check Tags of a Specific Repository
curl -u jacky:123456 https://192.168.2.130:5002/v2/hello-world/tags/list

# Expected output:
# {
#   "name": "hello-world",
#   "tags": ["latest"]
# }
```
