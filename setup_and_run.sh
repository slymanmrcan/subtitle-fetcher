#!/bin/bash

# YouTube Subtitle Downloader - Setup and Run Script

echo "--- Kurulum ve Çalıştırma Başlatılıyor ---"

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[1/3] Sanal ortam (venv) oluşturuluyor..."
    python3 -m venv venv
else
    echo "[1/3] Sanal ortam (venv) zaten mevcut."
fi

# 2. Install/Update requirements
echo "[2/3] Bağımlılıklar yükleniyor/güncelleniyor (yt-dlp en son versiyon)..."
./venv/bin/pip install -U pip
./venv/bin/pip install -U yt-dlp  # Explicitly upgrade yt-dlp
./venv/bin/pip install -r requirements.txt

# 3. Kill existing process on port 5000 (if any)
echo "Liman 5001 kontrol ediliyor..."
EXISTING_PID=$(lsof -ti:5001)
if [ ! -z "$EXISTING_PID" ]; then
    echo "5001 portundaki eski uygulama (PID: $EXISTING_PID) kapatılıyor..."
    kill -9 $EXISTING_PID
    sleep 1
fi

echo "[3/3] Uygulama başlatılıyor..."
echo "Tarayıcınızdan http://127.0.0.1:5001 adresine gidin."
./venv/bin/python app.py
