import os
import csv
from datetime import datetime
from io import BytesIO

from PIL import Image
import torch
from torchvision import transforms


IMG_SIZE = 224

# Transform used during inference
inference_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    """
    Convert raw image bytes to a normalized tensor suitable for model input.
    Returns a tensor of shape (1, C, H, W).
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    tensor = inference_transform(image).unsqueeze(0)
    return tensor


def ensure_logs_dir(base_dir: str) -> str:
    """
    Ensure that the logs directory exists under base_dir.
    Returns the absolute path to the logs directory.
    """
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def log_prediction(
    logs_dir: str,
    image_id: str,
    predicted_label: str,
    confidence: float,
):
    """
    Append prediction info to logs/predictions.csv.
    Columns: timestamp, image_id, predicted_label, confidence
    """
    file_path = os.path.join(logs_dir, "predictions.csv")
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "image_id", "predicted_label", "confidence"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            image_id,
            predicted_label,
            f"{confidence:.4f}",
        ])


def log_feedback(
    logs_dir: str,
    image_id: str,
    predicted_label: str,
    user_feedback: str,
    correct_label: str = "",
):
    """
    Append user feedback to logs/feedback.csv.
    Columns: timestamp, image_id, predicted_label, user_feedback, correct_label
    """
    file_path = os.path.join(logs_dir, "feedback.csv")
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "image_id", "predicted_label", "user_feedback", "correct_label"]
            )
        writer.writerow([
            datetime.utcnow().isoformat(),
            image_id,
            predicted_label,
            user_feedback,
            correct_label,
        ])
