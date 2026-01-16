import torch
import json
import os
from torchvision import models, transforms
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)


# Search paths for model files (local, dev, and Docker environments)
POSSIBLE_MODEL_PATHS = [
    os.path.join(PROJECT_ROOT, "model", "saved_models", "best_model.pth"),
    os.path.join(BASE_DIR, "model_files", "saved_models", "best_model.pth"),
    os.path.join("/app", "model_files", "saved_models", "best_model.pth"),
    os.path.join(BASE_DIR, "saved_models", "best_model.pth"),
]

POSSIBLE_CLASS_PATHS = [
    os.path.join(PROJECT_ROOT, "model", "saved_models", "class_indices.json"),
    os.path.join(BASE_DIR, "model_files", "saved_models", "class_indices.json"),
    os.path.join("/app", "model_files", "saved_models", "class_indices.json"),
    os.path.join(BASE_DIR, "saved_models", "class_indices.json"),
]

MODEL_PATH = None
CLASS_INDICES_PATH = None

for path in POSSIBLE_MODEL_PATHS:
    if os.path.exists(path):
        MODEL_PATH = path
        break

for path in POSSIBLE_CLASS_PATHS:
    if os.path.exists(path):
        CLASS_INDICES_PATH = path
        break


if MODEL_PATH is None:
    MODEL_PATH = POSSIBLE_MODEL_PATHS[0]
if CLASS_INDICES_PATH is None:
    CLASS_INDICES_PATH = POSSIBLE_CLASS_PATHS[0]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model_and_classes():
    """Load PyTorch model and class mappings for inference."""
    
    if not os.path.exists(CLASS_INDICES_PATH):
        tried_paths = "\n".join([f"  - {path}" for path in POSSIBLE_CLASS_PATHS])
        raise FileNotFoundError(
            f"Class indices file not found at: {CLASS_INDICES_PATH}\n"
            f"Tried the following paths:\n{tried_paths}\n"
            f"Current working directory: {os.getcwd()}\n"
            f"Backend directory: {BASE_DIR}\n"
            f"Please ensure the model files are in one of these locations."
        )
    if not os.path.exists(MODEL_PATH):
        tried_paths = "\n".join([f"  - {path}" for path in POSSIBLE_MODEL_PATHS])
        raise FileNotFoundError(
            f"Model file not found at: {MODEL_PATH}\n"
            f"Tried the following paths:\n{tried_paths}\n"
            f"Current working directory: {os.getcwd()}\n"
            f"Backend directory: {BASE_DIR}\n"
            f"Please ensure the model files are in one of these locations."
        )
    
    with open(CLASS_INDICES_PATH, "r") as f:
        class_indices = json.load(f)

    
    if not class_indices:
        raise ValueError(f"Class indices file is empty: {CLASS_INDICES_PATH}")

    
    first_key = list(class_indices.keys())[0]
    try:
        
        if str(first_key).isdigit():
            
            idx_to_class = {int(k): v for k, v in class_indices.items()}
        else:
            
            idx_to_class = {v: k for k, v in class_indices.items()}
    except Exception as e:
        raise ValueError(
            f"Failed to parse class indices. Expected format with numeric keys or reversed mapping. Error: {str(e)}"
        )

    num_classes = len(idx_to_class)

    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    except Exception as e:
        raise RuntimeError(
            f"Failed to load model from {MODEL_PATH}. Error: {str(e)}"
        )
    
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
    try:
        image = transform(image).unsqueeze(0).to(device)
    except Exception as e:
        raise ValueError(f"Failed to transform image: {str(e)}")

    with torch.no_grad():
        try:
            outputs = model(image)
            probs = torch.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probs, 1)
        except Exception as e:
            raise RuntimeError(f"Model prediction failed: {str(e)}")

    predicted_idx_value = predicted_idx.item()
    confidence_value = confidence.item()
    
    
    if predicted_idx_value not in idx_to_class:
        raise ValueError(
            f"Predicted class index {predicted_idx_value} not found in class mappings. "
            f"Available indices: {list(idx_to_class.keys())}"
        )

    return idx_to_class[predicted_idx_value], confidence_value