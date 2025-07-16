# Whisper API — 音檔轉文字服務

> 基於 [OpenAI Whisper](https://github.com/openai/whisper) 模型，提供簡易 RESTful API 與前端頁面，能將上傳的音訊檔（WAV/MP3…）即時轉成文字並回傳解析後的語音統計資訊。

---

## 功能特色

* **多語系辨識**：Whisper 支援多國語言，自動偵測語言並產生逐字稿。
* **JSON 結果**：除了轉錄文字，同步回傳語速、發音率、訊息量等統計指標。
* **Docker 化部署**：一鍵腳本完成模型下載、映像建置與容器啟動。
* **簡易前端**：提供可上傳檔案並顯示結果的網頁介面（如下圖）。

![UI Screenshot](docs/screenshot.png)

---

## 快速開始

### 1. 環境需求

| 需求                       | 最低版本          |
| ------------------------ | ------------- |
| Docker                   | 20.10+        |
| NVIDIA GPU 驅動            | 470.xx+（建議最新） |
| nvidia‑container‑toolkit | 任意可用版本        |

> 若無 GPU，也可改用 `cpu` 分支或自行在 Dockerfile 移除 `--gpus all`（速度較慢）。

### 2. 一鍵部署

```bash
# 進入專案根目錄（含此 README 與 run_whisper_api.sh）
chmod +x run_whisper_api.sh
./run_whisper_api.sh
```

腳本會自動：

1. 拉取 `python:3.10` 基礎映像。
2. 於臨時容器內安裝 Whisper 並執行 `download_model.py` 下載模型（預設 `large`）。
3. 建立 `whisper-api` Docker 映像。
4. 啟動 `whisper-api-container`，對外開放 [http://localhost:5005](http://localhost:5005)。

---

## API 介面

### `POST /transcribe`

| 參數   | 型別                   | 說明       |
| ---- | -------------------- | -------- |
| file | FormData (multipart) | 要轉錄的音訊檔案 |

**回傳範例**

```json
{
  "text": "這隻在一隻玩球把家裡的玻璃打破爸爸很生氣...",
  "stats": {
    "duration_sec": 26.46,
    "word_count": 74,
    "wpm": 167.8,
    "total_silence_sec": 0.56,
    "speech_time_sec": 25.9,
    "speech_rate_wpm": 171.43,
    "avg_silence_len_sec": 0.01,
    "avg_entropy_bits": 10.02,
    "bitrate_bps": 28.02
  }
}
```

* `text`：完整逐字稿。
* `stats`：語音分析指標。

### 錯誤碼

| HTTP 狀態 | 說明         |
| ------- | ---------- |
| 400     | 未提供檔案或格式錯誤 |
| 500     | 伺服器內部錯誤    |

---

## 手動流程（可選）

```bash
# 1. 下載模型
python download_model.py  # 需要先 pip install git+https://github.com/openai/whisper.git

# 2. 建立映像
docker build -t whisper-api .

# 3. 執行容器
docker run -dit --gpus all -p 5005:5000 --name whisper-api-container whisper-api
```

---

## 專案結構

```
Whisper/
├─ Dockerfile
├─ run_whisper_api.sh  # 一鍵部署腳本
├─ download_model.py   # 下載指定 whisper 模型
├─ app.py              # Flask/FastAPI 伺服器入口
├─ templates/          # 前端 HTML
├─ static/             # CSS / JS / 圖片
└─ docs/
   └─ screenshot.png   # UI 截圖
```

---

## 常見問題（FAQ）

<details>
<summary>Q1: 模型下載太慢或容量不足？</summary>
改編 `download_model.py` 傳入 `--model_size small` 或 `medium` 等參數；或將腳本中的 `download_model.py` 修改為較小模型。
</details>

<details>
<summary>Q2: 沒有 GPU 可以跑嗎？</summary>
可以。修改 `Dockerfile` 以 CPU-only 環境安裝 `torch` 與 `whisper`，並把 `docker run` 裡的 `--gpus all` 移除即可，惟速度會較慢。
</details>

---

## 授權

本專案採用 MIT License，詳見 `LICENSE` 檔案。
