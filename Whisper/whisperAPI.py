from flask import Flask, request, jsonify, render_template, send_file
import whisper
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import tempfile  # 用於創建臨時文件
from monpa import cut
import json
import math

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

def get_result_monpa(audio_file):
    # 進行語音辨識，設定需要詞語層級的時間戳記
    result = model.transcribe(audio_file, language="zh",
                              word_timestamps=True,
                              fp16=False, initial_prompt='在台灣的繁體中文漫畫中，我在圖中看到')

    # 提取字詞層級的資料
    segments = result['segments']
    words = []
    
    for segment in segments:
        for word_data in segment['words']:
            # 提取詞語和時間
            text = word_data["word"]
            start_time = word_data["start"]
            end_time = word_data["end"]

            # 如果詞語超過一個字，則進行拆分並均分時間
            if len(text) > 1:
                duration_per_char = (end_time - start_time) / len(text)
                for idx, char in enumerate(text):
                    char_start_time = start_time + idx * duration_per_char
                    char_end_time = char_start_time + duration_per_char
                    words.append({
                        "text": char,
                        "start": char_start_time,
                        "end": char_end_time
                    })
            else:
                # 單字詞直接加入
                words.append({
                    "text": text,
                    "start": start_time,
                    "end": end_time
                })
    # 提取所有字，方便做斷詞
    characters = [word["text"] for word in words]
    text = ''.join(characters)
    
    # 使用 monpa 進行斷詞
    seg_list = list(cut(text))
    # 初始化合併後的結果列表
    merged_results = []
    
    # 用來追蹤原始 words 中的位置
    i = 0
    for seg_word in seg_list:
        # 找到斷詞結果對應的字詞
        start_time = words[i]["start"]
        end_time = words[i + len(seg_word) - 1]["end"]
        merged_results.append({"text": seg_word, "start": start_time, "end": end_time})
        i += len(seg_word)
    
    # 返回結果
    return merged_results, text

def calculate_information_metrics(result, word_freq_dict):
    try:
        # 過濾不需要的詞
        merged_results = [
            r for r in result if r['text'] not in {',', ' ', '...'}
        ]

        total_words = len(merged_results)
        if total_words == 0:
            raise ValueError("No valid words to process")

        total_duration = merged_results[-1]['end'] - merged_results[0]['start']
        total_pause_time = sum(
            max(merged_results[i + 1]['start'] - merged_results[i]['end'], 0)
            for i in range(len(merged_results) - 1)
        )
        articulation_time = total_duration - total_pause_time

        # 語速和發音率
        speech_rate = (total_words / total_duration) * 60
        articulation_rate = (total_words / articulation_time) * 60

        # 平均停頓長度
        num_pauses = len(merged_results) - 1
        mean_pause_length = total_pause_time / num_pauses if num_pauses > 0 else 0

        # 熵和資訊率計算
        information_contents = []
        for item in merged_results:
            word = item['text']
            prob = word_freq_dict.get(word, 1)  # 防止 log(0)
            info_content = -math.log2(prob)
            information_contents.append(info_content)

        entropy = sum(information_contents) / total_words
        information_rate = sum(information_contents) / total_duration

        # 組裝結果
        return {
            'Total duration (seconds)': round(total_duration, 2),
            'Total number of words': total_words,
            'Speech rate (words/minute)': round(speech_rate, 2),
            'Total pause time (seconds)': round(total_pause_time, 2),
            'Articulation time (seconds)': round(articulation_time, 2),
            'Articulation rate (words/minute)': round(articulation_rate, 2),
            'Mean pause length (seconds)': round(mean_pause_length, 2),
            'Average information (entropy, bits)': round(entropy, 2),
            'Information rate (bits/second)': round(information_rate, 2)
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return {
            'Total duration (seconds)': -1,
            'Total number of words': -1,
            'Speech rate (words/minute)': -1,
            'Total pause time (seconds)': -1,
            'Articulation time (seconds)': -1,
            'Articulation rate (words/minute)': -1,
            'Mean pause length (seconds)': -1,
            'Average information (entropy, bits)': -1,
            'Information rate (bits/second)': -1
        }

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
            trimmed_audio = audio[start:]
        else:
            # 如果没有有效音讯，返回错误
            return jsonify({"error": "No non-silent segments detected."}), 400

        # 創建臨時文件保存處理後的音訊
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            trimmed_audio.export(temp_wav_file.name, format="wav")

            # Step2: 使用 get_result_monpa 函數獲取處理結果
            result, full_text = get_result_monpa(temp_wav_file.name)

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