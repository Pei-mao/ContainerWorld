#!/bin/bash

cd /NFS/PeiMao/GitHub/ContainerWorld/DataLab/env/JupyPytorch

docker build -t peimao/env/pytorch-notebook:latest . --no-cache

cd ..
cd ..

docker-compose build --no-cache

docker compose up -d