#!/usr/bin/env bash
# Author: PeiMao Sun
# Description: Build the custom PyTorch‑Notebook image and start the full DataLab stack.
# Usage: chmod +x run_datalab.sh && ./run_datalab.sh
# Note: This script should live **inside** the DataLab folder (alongside docker‑compose.yaml, env/, etc.).

set -e  # Exit immediately if a command exits with a non‑zero status.

# -------------------------------------------------
# Root directory of DataLab (the directory where this script resides)
# -------------------------------------------------
DATALAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# -------------------------------------------------
# Build the custom Jupyter Notebook image
# -------------------------------------------------
echo "[1/3] Building peimao/env/pytorch-notebook:latest …"
docker build --no-cache -t peimao/env/pytorch-notebook:latest "${DATALAB_DIR}/env/JupyPytorch"

# -------------------------------------------------
# Build all services defined in docker‑compose.yaml
# -------------------------------------------------
echo "[2/3] Building services via docker-compose …"
(cd "${DATALAB_DIR}" && docker-compose build --no-cache)

# -------------------------------------------------
# Start the stack
# -------------------------------------------------
echo "[3/3] Starting services …"
(cd "${DATALAB_DIR}" && docker-compose up -d)

echo "✅  DataLab stack is up. Visit JupyterHub at http://<host>:8000 (or the port configured in docker-compose)."
