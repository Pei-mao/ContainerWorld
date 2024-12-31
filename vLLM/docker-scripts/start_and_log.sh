#!/bin/bash

# 確保切換到包含 docker-compose.yaml 的目錄
cd ..

# 启动 Docker Compose
sudo docker-compose up -d

# 追踪日志
sudo docker logs -f vllm

