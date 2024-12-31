# vLLM Project

This project is a vLLM deployment system based on Docker and Hugging Face models, designed for quickly setting up and testing inference services for language models.

## Project Structure

```plaintext
├── docker-compose.yaml       # Docker Compose configuration file
├── docker-scripts/           # Directory for setup and utility scripts
│   ├── setup_vllm.sh         # Script to set up the vLLM system
│   ├── start_and_log.sh      # Script to start Docker and monitor logs
├── models/                   # Directory for Hugging Face models
│   └── Qwen2.5-7B-Instruct   # Downloaded model directory
├── call_API.py               # Python script to test API calls
├── README.md                 # Project documentation file
```

## Installation and Setup

1. **Prepare the Environment**
   - Ensure Docker and Docker Compose are installed on your system.

2. **Run the Setup Script**

   Execute `setup_vllm.sh` to install dependencies and download the model:

   ```bash
   bash docker-scripts/setup_vllm.sh
   ```

3. **Start the Service**

   Use `start_and_log.sh` to start the Docker container and monitor logs:

   ```bash
   bash docker-scripts/start_and_log.sh
   ```

## Testing API Calls

Use `call_API.py` to test model inference:

```bash
python3 call_API.py
```

This script sends input to the service and returns the model-generated response. Ensure the service is running and matches the configuration in `docker-compose.yaml`.

## Docker Configuration

The `docker-compose.yaml` defines the following:
- Model used: `Qwen2.5-7B-Instruct`
- Container name: `vllm`
- Exposed port: `8000`
- GPU memory utilization: `70%`

## Notes

1. Ensure the `models` folder contains the correct Hugging Face model files.
2. If Docker fails to start, check if your GPU drivers and NVIDIA Docker are correctly installed.

## Project Diagram

Below is a system architecture diagram:

![Architecture Diagram](image.png)

## Contact

If you have any questions, please contact the project maintainer or submit an issue.
