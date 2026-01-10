import torch
import json
import os
from torchvision import models, transforms
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "best_model.pth")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "saved_models", "class_indices.json")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model_and_classes():
    with open(CLASS_INDICES_PATH, "r") as f:
        class_indices = json.load(f)

    # Handle both formats
    if not list(class_indices.keys())[0].isdigit():
        idx_to_class = {v: k for k, v in class_indices.items()}
    else:
        idx_to_class = {int(k): v for k, v in class_indices.items()}

    num_classes = len(idx_to_class)

    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()

    return model, idx_to_class


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(model, idx_to_class, image: Image.Image):
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probs, 1)

    return idx_to_class[predicted_idx.item()], confidence.item()

