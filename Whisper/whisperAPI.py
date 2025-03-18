from flask import Flask, request, jsonify, render_template, send_file
import whisper
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import tempfile  # 用於創建臨時文件
from monpa import cut
import json
from utils import get_result_monpa, calculate_information_metrics


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

        # Step1: 使用 pydub 去除音频文件的静音部分
        audio = AudioSegment.from_file(file_path)
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)

        if nonsilent_ranges:
            # 裁剪掉静音部分
            start, _ = nonsilent_ranges[0]
            cut_off_time = start
            trimmed_audio = audio[start:]
        else:
            # 如果没有有效音讯，返回错误
            return jsonify({"error": "No non-silent segments detected."}), 400

        # 創建臨時文件保存處理後的音訊
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            trimmed_audio.export(temp_wav_file.name, format="wav")

            # Step2: 使用 get_result_monpa 函數獲取處理結果
            result, full_text = get_result_monpa(temp_wav_file.name, model)

        # 加載詞頻表
        with open('SUBTLEX-CH-WF-traditional.json', 'r', encoding='utf-8') as f:
    	    word_freq_dict = json.load(f)

        # 確保詞頻總和為 1，進行正規化
        # 計算總頻數
        total_freq = sum(word_freq_dict.values())
        # 計算每個詞的概率
        for word in word_freq_dict:
            word_freq_dict[word] /= total_freq

        # Step3: 計算資訊指標
        information_metrics = calculate_information_metrics(result, word_freq_dict)

        # 保存結果為 JSON 文件
        json_file_path = os.path.splitext(file_path)[0] + "_result.json"
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)

        # 同時返回轉錄結果和下載鏈接
        response = {
            "transcription_result": full_text,
            "information_metrics": information_metrics,
            "cut_off_time_ms": cut_off_time,
            "download_url": f"/download/{os.path.basename(json_file_path)}"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

# 提供下載 JSON 文件的路由
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found."}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)