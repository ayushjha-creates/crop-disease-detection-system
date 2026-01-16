from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
from PIL import Image
import io
import traceback

from app import predict_image, load_model_and_classes
from recommendation_engine import RECOMMENDATIONS

app = FastAPI(title="Crop Disease Detection API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and classes
model = None
idx_to_class = None

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    global model, idx_to_class
    try:
        print("Loading model and class mappings...")
        model, idx_to_class = load_model_and_classes()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load model: {str(e)}")
        print(traceback.format_exc())

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Crop Disease Detection API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if model is None:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": "Model not loaded"}
        )
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    """Predict crop disease from uploaded image."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Make prediction
        prediction, confidence = predict_image(model, idx_to_class, image)
        
        # Get recommendations for the predicted disease
        recommendation = RECOMMENDATIONS.get(prediction, {})
        
        # Extract crop and disease names from prediction
        if "___" in prediction:
            crop_name, disease_name = prediction.split("___", 1)
        else:
            crop_name = prediction
            disease_name = "Unknown"
        
        response_data = {
            "predicted_class": prediction,
            "crop_name": crop_name,
            "disease_name": disease_name,
            "confidence": confidence,
            "status": "success",
            "description": recommendation.get("disease_description", "No description available"),
            "symptoms": recommendation.get("symptoms", "No symptoms information available"),
            "organic": recommendation.get("treatment_organic", "No organic treatment available"),
            "chemical": recommendation.get("treatment_chemical", "No chemical treatment available"),
            "preventive": recommendation.get("preventive_measures", "No preventive measures available")
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)