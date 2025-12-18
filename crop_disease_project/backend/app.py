from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from model_loader import load_model_and_classes, predict_image
from recommendation_engine import get_recommendation


app = FastAPI(
    title="Crop Disease Detection API",
    version="1.0.0"
)

# ✅ CORS (frontend fix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
model, idx_to_class = load_model_and_classes()


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Predict
    predicted_class, confidence = predict_image(
        model, idx_to_class, image
    )

    # ✅ SPLIT crop and disease
    if "___" in predicted_class:
        crop_name, disease_name = predicted_class.split("___", 1)
    else:
        crop_name = predicted_class
        disease_name = " "

    # ✅ GET RECOMMENDATION
    recommendation = get_recommendation(crop_name, disease_name)

    # ✅ RETURN RESPONSE (INSIDE FUNCTION)
    return {
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "crop_name": crop_name,
        "disease_name": disease_name if disease_name else "Healthy",
        "recommendation": recommendation
    }

