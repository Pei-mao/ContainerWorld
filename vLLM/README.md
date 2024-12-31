# vLLM Project

本專案是基於 Docker 與 Hugging Face 模型的 vLLM 部署系統，用於快速搭建並測試語言模型的推論服務。

## 專案結構

```plaintext
├── docker-compose.yaml   # Docker Compose 配置文件
├── start_and_log.sh      # 啟動 Docker 並追蹤日誌的腳本
├── setup_vllm.sh         # vLLM 系統設置腳本
├── call_API.py           # 測試 API 調用的 Python 腳本
├── models/               # Hugging Face 模型存放目錄
├── README.md             # 專案說明文件
```

## 安裝與設置

1. **準備環境**
   - 確保您的系統已安裝 Docker 與 Docker Compose。

2. **執行設置腳本**

   運行 `setup_vllm.sh` 安裝必要的依賴與下載模型：

   ```bash
   bash setup_vllm.sh
   ```

3. **啟動服務**

   使用 `start_and_log.sh` 啟動 Docker 容器並檢視日誌：

   ```bash
   bash start_and_log.sh
   ```

## 測試 API 調用

使用 `call_API.py` 測試模型推論：

```bash
python3 call_API.py
```

此腳本將發送內容至服務並返回模型生成的響應。確保服務已啟動並與 `docker-compose.yaml` 中的配置一致。

## Docker 配置

`docker-compose.yaml` 定義了以下內容：
- 使用的模型：`Qwen2.5-7B-Instruct`
- 容器名稱：`vllm`
- 暴露的端口：`8000`
- GPU 記憶體利用率：`70%`

## 注意事項

1. 請確保 `models` 資料夾中包含正確的 Hugging Face 模型文件。
2. 若 Docker 無法正確啟動，請檢查 GPU 驅動與 NVIDIA Docker 是否已正確安裝。

## 項目截圖

以下為系統架構的示意圖：

![架構圖](image.png)

## 聯繫方式

若有任何問題，請聯繫專案維護者或提交 Issue。