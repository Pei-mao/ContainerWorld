# 使用官方 Python 映像作為基礎
FROM python:3.10

# 安裝 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# 設置工作目錄
WORKDIR /app

# 複製應用程式代碼到容器內
COPY whisperAPI.py /app/whisperAPI.py
COPY templates/index.html /app/templates/index.html

# 複製本地已下載的模型到容器內
COPY models /app/models

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir flask openai-whisper

# 預先下載 Whisper 模型
#RUN python -c "import whisper; whisper.load_model('base')"

# 開放應用使用的埠
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "whisperAPI.py"]

