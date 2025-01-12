from flask import Flask, request, jsonify, render_template
import whisper
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import tempfile  # 用於創建臨時文件

app = Flask(__name__)

# 加载 Whisper 模型
model = whisper.load_model("large-v3", download_root='./models')

# 设置上传文件的保存路径
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 首页路由，显示上传表单
@app.route('/')
def index():
    return render_template('index.html')

# 处理音频文件上传和转录
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # 如果用户没有选择文件
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # 保存上传的文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 使用 pydub 去除音频文件的静音部分
        audio = AudioSegment.from_file(file_path, format="wav")
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)

        if nonsilent_ranges:
            # 裁剪掉静音部分
            start, _ = nonsilent_ranges[0]
            trimmed_audio = audio[start:]
        else:
            # 如果没有有效音讯，返回错误
            return jsonify({"error": "No non-silent segments detected."}), 400

        # 創建臨時文件保存處理後的音訊
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            trimmed_audio.export(temp_wav_file.name, format="wav")
            
            # 使用 Whisper 模型轉錄臨時文件
            result = model.transcribe(temp_wav_file.name)

        return jsonify({"text": result["text"]})

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
