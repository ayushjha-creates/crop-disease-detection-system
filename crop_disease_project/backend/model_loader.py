import torch
import json
import os
from torchvision import models, transforms
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "saved_models", "best_model.pth")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "model", "saved_models", "class_indices.json")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model_and_classes():
    # Load class indices
    with open(CLASS_INDICES_PATH, "r") as f:
        class_indices = json.load(f)

    # FIX: if keys are class names, reverse mapping
    if not list(class_indices.keys())[0].isdigit():
        idx_to_class = {v: k for k, v in class_indices.items()}
    else:
        idx_to_class = {int(k): v for k, v in class_indices.items()}

    num_classes = len(idx_to_class)

    # Load model
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()

    return model, idx_to_class


# Image preprocessing
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

    predicted_class = idx_to_class[predicted_idx.item()]

    return predicted_class, confidence.item()


