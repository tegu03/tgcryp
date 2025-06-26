# train_model.py
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import json
from model.ChartClassifier import ChartClassifier

class ChartDataset(Dataset):
    def __init__(self, label_file, image_dir, transform=None):
        with open(label_file, 'r') as f:
            self.data = json.load(f)
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data[idx]
        image_path = os.path.join(self.image_dir, row["filename"])
        image = Image.open(image_path).convert("RGB")
        label = 0 if row["type"] == "long" else 1

        if self.transform:
            image = self.transform(image)

        return image, label

# Config
label_path = "dataset/labels.json"
image_path = "dataset/images"
batch_size = 8
num_epochs = 10

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Dataset
dataset = ChartDataset(label_path, image_path, transform)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Model
model = ChartClassifier(num_classes=2)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Training
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

print("Training started...")

for epoch in range(num_epochs):
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        preds = model(images)
        loss = loss_fn(preds, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{num_epochs} - Loss: {loss.item():.4f}")

# Save
os.makedirs("model", exist_ok=True)
torch.save(model.state_dict(), "model/chart_model.pt")
print("Training complete. Model saved to model/chart_model.pt")
