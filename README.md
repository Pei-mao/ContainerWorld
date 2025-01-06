# ContainerWorld 🌍

Welcome to **ContainerWorld**, a comprehensive collection of containerized projects designed to simplify development, deployment, and management of applications. This repository serves as a one-stop solution for exploring various real-world use cases of containerization technology.

## 📦 Current Projects

### 1. **Registry**  
A private container registry for securely hosting and managing your Docker images.
- Support for `HTTPS (TLS)` for secure connections.
- `Basic authentication` for access control.
- Easy setup using `Docker` or `Docker Compose`.  
[Learn More About Registry](Registry/README.md)

### 2. **JupyterhubDock (WIP)**  
A scalable, containerized JupyterHub environment for collaborative development.
- Multi-user support: Enable multiple users to work simultaneously with individual environments.
- DockerSpawner integration: Isolate each user's environment using Docker containers.
- Resource control: Limit CPU and memory usage for each user to ensure system stability.
- Customizable images: Use pre-built or custom Docker images for diverse development needs.  
[Learn More About JupyterhubDock](JupyterhubDock/README.md)

### 3. **OllamaLLM**  
A containerized deployment of large language models (LLMs) as APIs using `Ollama`.
- Run local large language models with API endpoints for seamless integration.
- Utilize `AnythingLLM` for a GUI interface, offering an intuitive way to interact with LLMs.
- Easily switch between different pre-trained LLMs or fine-tuned models.  
[Learn More About OllamaLLM](OllamaLLM/README.md)

### 4. **vLLM**

The vLLM-based API provides efficient and flexible inference for large language models.
- Rapid setup with Docker (`docker-compose.yaml`), supporting custom models like `Qwen2.5-7B-Instruct`.
- GPU acceleration with adjustable memory usage for stable operation.
- OpenAI-style HTTP interface for easy integration, with example scripts like `call_API.py`.
- Supports chatbots, content generation, and question answering for complex queries like "What is DeepVBM?"  
[Learn More About vLLM](vLLM/README.md)

### 5. **Portainer**

Portainer provides an intuitive interface for managing and monitoring `Docker containers`.
- Real-time resource monitoring for `CPU` and `memory` usage.
- Simple container control for starting, stopping, and managing Docker environments.  
[Learn More About Portainer](Portainer/README.md)

### 6. **Whisper**

WhisperAPI offers a containerized Speech-to-Text API using OpenAI's Whisper model.
- Easy-to-deploy `Docker` setup for hosting the API locally or on the cloud.
- Real-time transcription of audio files into text via an intuitive `HTTP POST` interface.
- Compatibility with various audio formats and support for `Dockerized` environments.
- Includes sample commands for API testing, such as `curl` examples, for rapid integration.  
[Learn More About Whisper](Whisper/README.md)

---

## 🚀 Why ContainerWorld?

- **Learn by Examples**: Each project is a hands-on implementation of containerized solutions.
- **Diverse Use Cases**: From hosting private registries to deploying complex multi-service applications.
- **Modular and Reusable**: Easily adapt the setups for your own projects.
- **Beginner-Friendly**: Step-by-step guides and detailed documentation for each project.

---

## 🛠 How to Get Started

1. Clone this repository:
   ```bash
   git clone https://github.com/Pei-mao/ContainerWorld.git
   cd ContainerWorld
   
