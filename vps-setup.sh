#!/bin/bash

echo "[1/5] Update dan install dependensi sistem..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-full python3-venv python3-pip ffmpeg screen

echo "[2/5] Clone repo (jika belum)..."
if [ ! -d "tgcryp" ]; then
  git clone https://github.com/tegu03/tgcryp.git
fi
cd tgcryp || exit 1

echo "[3/5] Setup virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[4/5] Install Python dependencies..."
pip install --upgrade pip
pip install torch torchvision pillow python-dotenv python-telegram-bot

echo "[5/5] Jalankan training AI..."
python train_model.py

echo "✅ Setup selesai."
echo "➡️ Jalankan bot dengan: screen -S tgcrypbot bash run-bot.sh"
