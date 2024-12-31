# Portainer Setup and Overview

## Introduction
Portainer is a lightweight management UI for Docker that allows you to easily manage your Docker environments. This guide provides the steps to set up Portainer using Docker, along with an overview of its features.

## Features

- **Dashboard**: Monitor your Docker environment, including stacks, containers, images, volumes, and networks.
  ![Dashboard](./Dashboard.PNG)

- **New Installation**: Create a secure admin user for your Portainer setup.
  ![New Installation](./Entrance.PNG)

- **Resource Monitoring**: Track CPU, memory, network, and I/O usage of containers in real-time.
  ![Resource Monitoring](./Resource_monitoring.PNG)

## Prerequisites

- Docker must be installed on your system.

## Setup Instructions

### Step 1: Download the Script
Ensure you have the `run_portainer.sh` script in your working directory.

### Step 2: Run the Setup Script
Execute the following command in your terminal:

```bash
bash run_portainer.sh
```

### Step 3: Access Portainer
Once the setup is complete, access the Portainer UI by visiting:

```
http://localhost:9000
```

### Script Details
The `run_portainer.sh` script performs the following actions:

1. Checks if Docker is installed.
2. Stops and removes any existing Portainer container.
3. Pulls and runs the Portainer container on ports `8000` and `9000`.
4. Ensures the container restarts automatically if the system reboots.

The script uses the following Docker parameters:

- **Port Mapping**:
  - `8000`: Agent communication
  - `9000`: Web interface
- **Volume Mapping**:
  - `/var/run/docker.sock`: Access to Docker socket
  - `portainer_data`: Persistent data storage

## Troubleshooting

If the container fails to start, review the logs using:

```bash
docker logs portainer
```

## Files in This Repository

- `run_portainer.sh`: Script to set up and run Portainer.
- `Dashboard.PNG`: Portainer dashboard screenshot.
- `Entrance.PNG`: Initial setup screenshot.
- `Resource_monitoring.PNG`: Resource monitoring screenshot.

## Notes
- Ensure your Docker installation is up-to-date.
- Use strong passwords when setting up the admin user.

---

Feel free to explore the Portainer interface to manage your Docker containers effectively!