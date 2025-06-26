# bot/analyzer.py
import torch
from PIL import Image
from torchvision import transforms
from model.ChartClassifier import ChartClassifier

# Load model
model = ChartClassifier(num_classes=2)
model.load_state_dict(torch.load("model/chart_model.pt", map_location=torch.device("cpu")))
model.eval()

# Image preprocessor
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def analyze_chart(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()
        signal = "LONG 🔼" if prediction == 0 else "SHORT 🔽"

    # Dummy SL/TP sementara
    sl = "Auto SL: 1.5% dari Entry"
    tp = "Auto TP: 3.5% dari Entry"

    return f"""
📊 Hasil Analisis Chart:

🔹 Rekomendasi Entry: {signal}
🔹 {sl}
🔹 {tp}

📈 Pola Terdeteksi: Berdasarkan pembelajaran AI dari data historis
🤖 Sumber: Gambar chart (model AI training)

⚠️ *Jangan Greedy!*
💰 *Gunakan Money Management*
📉 *Open posisi maksimal 10% dari modal*
"""
