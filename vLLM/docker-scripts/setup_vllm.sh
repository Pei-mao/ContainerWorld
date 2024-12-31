#!/bin/bash

# Update the system and install Git LFS
sudo apt update
sudo apt install -y git-lfs

git lfs install

# Pull the vLLM Docker image
sudo docker pull vllm/vllm-openai:v0.6.1

# Clone the Qwen2.5-7B-Instruct model from Hugging Face
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

# Create models directory in the parent folder and move the model
mkdir -p ../models
sudo mv Qwen2.5-7B-Instruct ../models/Qwen2.5-7B-Instruct

echo "Setup completed successfully."
