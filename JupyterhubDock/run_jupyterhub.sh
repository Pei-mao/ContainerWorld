#!/bin/bash

cd /NFS/PeiMao/GitHub/ContainerWorld/JupyterhubDock

docker network create jupyterhub-network

docker build -t my-jupyterhub .

docker run -d -p 8000:8000 --name jupyterhub \
        -v /var/run/docker.sock:/var/run/docker.sock \
	-v /NFS/PeiMao/GitHub/ContainerWorld/JupyterhubDock/config/jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py \
    	-v /NFS:/NFS \
	--network=jupyterhub-network \
	my-jupyterhub
