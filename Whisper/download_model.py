import whisper

# 指定保存模型的路徑
model_dir = "./models"
model_name = "base"
#model_name = "large-v3"

# 下載模型
whisper.load_model(model_name, download_root=model_dir)
