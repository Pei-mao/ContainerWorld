#!/bin/bash

# 列出可用的模型
echo "Listing available Ollama models:"
ollama list

# 運行 8B 模型
echo "Running Llama-3-Taiwan-8B-Instruct-gguf..."
ollama run hf.co/RichardErkhov/yentinglin_-_Llama-3-Taiwan-8B-Instruct-gguf

# 運行 70B 模型
echo "Running Llama-3-Taiwan-70B-Instruct-gguf..."
ollama run hf.co/RichardErkhov/yentinglin_-_Llama-3-Taiwan-70B-Instruct-gguf

# 結束訊息
echo "Script execution completed."
