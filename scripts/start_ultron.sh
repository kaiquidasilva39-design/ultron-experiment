#!/data/data/com.termux/files/usr/bin/bash

cd "$HOME/ultron-experiment"

if ! curl -s --max-time 2 http://127.0.0.1:8080/health >/dev/null 2>&1; then
    nohup "$HOME/ultron-experiment/scripts/start_ai.sh" \
        > "$HOME/ultron-experiment/data/llama-server.log" 2>&1 &
fi

sleep 3

exec python -m app.final_runtime
