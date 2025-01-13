import math
from monpa import cut

def get_result_monpa(audio_file, model):
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
            'Information rate (bits/second)': round(information_rate, 2)}
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
