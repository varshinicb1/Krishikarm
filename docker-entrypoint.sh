#!/bin/bash
# ============================================================
# Kisan-Eye V6 — Production Entrypoint
# Serves backend API + built frontend on single port 8000
# ============================================================

set -e

echo "🛰️  Kisan-Eye V6 — Village Kiosk AI"
echo "══════════════════════════════════════"
echo "  LLM:      ${LLM_MODEL:-llama3} @ ${OLLAMA_URL:-http://localhost:11434}"
echo "  Whisper:   ${WHISPER_MODEL:-medium}"
echo "  Frontend:  ${FRONTEND_DIR:-/app/frontend}"
echo "══════════════════════════════════════"

# Wait for Ollama to be reachable
echo "⏳ Waiting for Ollama..."
for i in $(seq 1 30); do
    if curl -sf "${OLLAMA_URL:-http://localhost:11434}/api/tags" > /dev/null 2>&1; then
        echo "✅ Ollama connected"
        break
    fi
    sleep 2
done

# Start the unified server (API + static frontend)
cd /app/backend
echo "🚀 Starting Kisan-Eye on :8000..."
exec python3 -m uvicorn server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    --workers 1 \
    --timeout-keep-alive 120
