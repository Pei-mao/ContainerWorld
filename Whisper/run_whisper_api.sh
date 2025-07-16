#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------
# Whisper API 部署腳本 (置於 Whisper 專案根目錄)
# -----------------------------------------------------------
# 使用方式：
#   1. 將此檔放在 Whisper 專案目錄中 (與 Dockerfile、download_model.py 等同級)。
#   2. 賦予執行權限： chmod +x run_whisper_api.sh
#   3. 執行腳本：      ./run_whisper_api.sh
#
# 需求：
#   - Docker 與 GPU 支援 (nvidia-container-toolkit)
# -----------------------------------------------------------

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="whisper-api"
CONTAINER_NAME="whisper-api-container"
HOST_PORT=5005
CONTAINER_PORT=5000

cd "${PROJECT_DIR}"

echo "🔹 拉取 Python 3.10 映像..."
docker pull python:3.10

echo "🔹 使用臨時容器下載 Whisper 模型 (避免本機安裝依賴)..."
docker run --rm \
           -v "${PROJECT_DIR}":/workspace \
           -w /workspace \
           python:3.10 \
           bash -c "pip install -q git+https://github.com/openai/whisper.git && python download_model.py"

echo "🔹 建立 Docker 映像 (${IMAGE_NAME})..."
docker build -t "${IMAGE_NAME}" .

echo "🔹 檢查是否已有同名容器..."
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "   已存在同名容器，將其移除..."
  docker rm -f "${CONTAINER_NAME}"
fi

echo "🔹 啟動 Whisper API 容器..."
docker run -dit --gpus all -p "${HOST_PORT}:${CONTAINER_PORT}" --name "${CONTAINER_NAME}" "${IMAGE_NAME}"

echo "✅ 部署完成！您可使用下列指令測試服務："
echo "curl -X POST \"http://localhost:${HOST_PORT}/transcribe\" -F \"file=@test_music.wav\""