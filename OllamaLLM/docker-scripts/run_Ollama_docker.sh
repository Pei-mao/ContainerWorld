#!/bin/bash

# Pull the latest Ollama image from Docker Hub
docker pull ollama/ollama:latest

# Run a Docker container with Ollama and map the required ports and volumes
docker run -d \
	  --gpus=all \
	    -v /NFS/PeiMao/GitHub/ContainerWorld/OllamaLLM/ollama:/root/.ollama:z \
	      -p 11434:11434 \
	        --name my_ollama \
		  ollama/ollama

# Enter the container interactively to check its status or run commands
docker exec -it my_ollama /bin/bash
