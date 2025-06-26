#!/bin/bash

echo "[1/5] Update dan install dependensi sistem..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-full python3-venv python3-pip ffmpeg

echo "[2/5] Clone repo tgcryp..."
git clone https://github.com/tegu03/tgcryp.git
cd tgcryp || exit 1

echo "[3/5] Buat dan aktifkan virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[4/5] Install dependensi Python..."
pip install --upgrade pip
pip install torch torchvision pillow python-dotenv python-telegram-bot

echo "[5/5] Training AI..."
python train_model.py

echo "✅ Setup selesai. Jalankan bot dengan:"
echo "source venv/bin/activate && python bot/main.py"
