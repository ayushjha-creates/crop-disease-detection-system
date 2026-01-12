from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from model_loader import load_model_and_classes, predict_image
from recommendation_engine import get_recommendation

app = FastAPI(
    title="Crop Disease Detection API",
    version="1.0.0"
)


# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model and class mappings on startup
model, idx_to_class = load_model_and_classes()

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        if file.content_type and file.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/bmp"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {file.content_type}. Please upload an image (JPEG, PNG, or BMP)."
            )
        
        image_bytes = await file.read()
        
        if not image_bytes or len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to process image file. Please ensure the file is a valid image. Error: {str(e)}"
            )
        
        # Predict
        try:
            predicted_class, confidence = predict_image(
                model, idx_to_class, image
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during prediction: {str(e)}"
            )

        # Extract crop and disease from class name
        if "___" in predicted_class:
            crop_name, disease_name = predicted_class.split("___", 1)
        else:
            crop_name = predicted_class
            disease_name = " "

        # Get treatment recommendation
        recommendation = get_recommendation(crop_name, disease_name)

        #  RETURN RESPONSE (INSIDE FUNCTION)
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4),
            "crop_name": crop_name,
            "disease_name": disease_name if disease_name else "Healthy",
            "recommendation": recommendation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

