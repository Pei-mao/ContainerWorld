# 定義存儲路徑
STORAGE_LOCATION=/NFS/PeiMao/GitHub/ContainerWorld/OllamaLLM/anythingllm

# 創建存儲資料夾
mkdir -p $STORAGE_LOCATION

# 創建 .env 文件
if [ ! -f "$STORAGE_LOCATION/.env" ]; then
	  touch "$STORAGE_LOCATION/.env"
fi

# 運行 Docker 容器
docker run -d -p 3001:3001 \
	  --name my_anythingllm \
	    --cap-add SYS_ADMIN \
	      -v ${STORAGE_LOCATION}:/app/server/storage \
	        -v ${STORAGE_LOCATION}/.env:/app/server/.env \
		  -e STORAGE_DIR="/app/server/storage" \
		    mintplexlabs/anythingllm
