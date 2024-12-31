#!/bin/bash

# 檢查是否已經安裝 Docker
if ! command -v docker &> /dev/null; then
	    echo "Docker 未安裝，請先安裝 Docker。"
	        exit 1
fi

# 設定變數
CONTAINER_NAME="portainer"
PORTAINER_IMAGE="portainer/portainer"
DATA_VOLUME="portainer_data"
DOCKER_SOCK="/var/run/docker.sock"

# 停止並刪除已存在的容器
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
	    echo "已有名為 $CONTAINER_NAME 的容器，正在刪除..."
	        docker stop $CONTAINER_NAME
		    docker rm $CONTAINER_NAME
fi

# 執行 Docker 命令
echo "啟動 $CONTAINER_NAME 容器..."
docker run -d -p 8001:8000 -p 9000:9000 \
	    --name $CONTAINER_NAME --restart=always \
	        -v $DOCKER_SOCK:$DOCKER_SOCK \
		    -v $DATA_VOLUME:/data \
		        $PORTAINER_IMAGE

# 檢查容器是否啟動成功
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
	    echo "$CONTAINER_NAME 已成功啟動。"
    else
	        echo "$CONTAINER_NAME 啟動失敗，請檢查日誌。"
		    exit 1
fi
