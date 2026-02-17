# ============================================================
# Kisan-Eye V6 — Production Dockerfile
# GPU-accelerated village kiosk AI (Face + Voice + LLM + Satellite)
# ============================================================

# ===== Stage 1: Build frontend with Vite =====
FROM node:20-slim AS frontend
WORKDIR /build

# Install deps
COPY package.json package-lock.json ./
RUN npm ci

# Copy source and build
COPY index.html main.js kiosk.js style.css v5_features.js vite.config.js ./
COPY public/ ./public/

# Vite build → /build/dist
RUN npm run build

# ===== Stage 2: Python backend + built frontend =====
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04 AS production

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip python3.11-dev \
    libgl1-mesa-glx libglib2.0-0 \
    curl wget ffmpeg \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps (install before copying code for layer caching)
COPY backend/requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt \
    && pip3 install --no-cache-dir --break-system-packages piper-tts 2>/dev/null || true

# Copy backend
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend /build/dist/ ./frontend/

# Entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Single port for everything
EXPOSE 8000

# Environment
ENV OLLAMA_URL=http://ollama:11434
ENV LLM_MODEL=llama3
ENV WHISPER_MODEL=medium
ENV FRONTEND_DIR=/app/frontend

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]
