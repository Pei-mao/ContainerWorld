from flask import Flask, request, jsonify, render_template
import whisper
import os

app = Flask(__name__)

# 加载 Whisper 模型
model = whisper.load_model("base")

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

        # 使用 Whisper 模型转录音频
        result = model.transcribe(file_path)

        # 删除临时保存的文件
        os.remove(file_path)

        return jsonify({"text": result["text"]})

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

