# 使用官方 Python 映像作為基礎
FROM python:3.10

# 安裝 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# 設置工作目錄
WORKDIR /app

# 複製應用程式代碼到容器內
COPY . .

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir flask openai-whisper

# 開放應用使用的埠
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "whisperAPI.py"]

