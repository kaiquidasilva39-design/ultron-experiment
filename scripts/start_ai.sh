#!/data/data/com.termux/files/usr/bin/bash

MODEL="$HOME/llama.cpp/models/Qwen3-0.6B-Q4_0.gguf"
SERVER="$HOME/llama.cpp/build/bin/llama-server"

exec "$SERVER" \
  -m "$MODEL" \
  --host 127.0.0.1 \
  --port 8080 \
  -c 1024 \
  -n 256
