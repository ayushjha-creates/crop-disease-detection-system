# Crop Disease Predictor

A deep learning-based web application for identifying crop diseases from plant leaf images and providing treatment recommendations.

## Project Structure

```
crop_disease_project/
├── backend/              # Flask API server
│   ├── app.py           # Main Flask application
│   ├── model_loader.py  # Model loading and prediction logic
│   ├── recommendation_engine.py  # Treatment recommendations
│   ├── utils.py         # Utility functions
│   └── requirements.txt # Python dependencies
├── model/               # Model training scripts
│   ├── train_model.py   # Training script
│   ├── dataset_loader.py  # Dataset loading utilities
│   ├── config.py        # Training configuration
│   └── saved_models/    # Trained model files
│       ├── best_model.pth
│       └── class_indices.json
├── frontend/            # Web interface
│   ├── index.html       # Main HTML page
│   ├── styles.css       # Styling
│   └── app.js          # Frontend JavaScript
├── data/                # Dataset storage
│   └── raw/
│       └── new-plant-diseases-dataset/
│           ├── train/   # Training images
│           ├── valid/   # Validation images
│           └── test/    # Test images
├── logs/                # Application logs
│   ├── predictions.csv  # Prediction history
│   └── feedback.csv     # User feedback
└── README.md           # This file
```

## Features

- **Disease Detection**: Upload plant leaf images to identify diseases using a deep learning model
- **Treatment Recommendations**: Get detailed treatment steps and prevention tips for identified diseases
- **Confidence Scores**: View prediction confidence levels
- **User Feedback**: Provide feedback on predictions to improve the system
- **Responsive Design**: Modern, mobile-friendly web interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- CUDA-capable GPU (optional, for faster training and inference)
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation

### 1. Clone or Download the Repository

```bash
cd crop_disease_project
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Prepare the Dataset

1. Download the New Plant Diseases Dataset
2. Extract it to `data/raw/new-plant-diseases-dataset/`
3. Ensure the structure matches:
   ```
   data/raw/new-plant-diseases-dataset/
   ├── train/
   │   ├── class1/
   │   ├── class2/
   │   └── ...
   ├── valid/
   │   ├── class1/
   │   ├── class2/
   │   └── ...
   └── test/
       ├── class1/
       ├── class2/
       └── ...
   ```

## Usage

### Training the Model

1. Update configuration in `model/config.py` if needed
2. Run the training script:

```bash
cd model
python train_model.py
```

The trained model will be saved to `model/saved_models/best_model.pth`

### Running the Backend Server

1. Make sure the trained model exists in `model/saved_models/`
2. Start the Flask server:

```bash
cd backend
python app.py
```

The API server will run on `http://localhost:5000`

### Running the Frontend

1. Open `frontend/index.html` in your web browser
   - Or use a local web server:
   
```bash
cd frontend
python -m http.server 8000
```

2. Navigate to `http://localhost:8000` in your browser

### Using the Application

1. Click the upload area or drag and drop an image of a plant leaf
2. Click "Analyze Disease" to get predictions
3. Review the disease identification and treatment recommendations
4. Optionally provide feedback on the prediction

## API Endpoints

### Health Check
```
GET /health
```
Returns API health status.

### Predict Disease
```
POST /predict
Content-Type: multipart/form-data
Body: image file
```
Returns disease prediction and recommendations.

### Submit Feedback
```
POST /feedback
Content-Type: application/json
Body: {
    "prediction_id": "string",
    "rating": "helpful" | "not-helpful",
    "comment": "string",
    "predicted_class": "string",
    "actual_class": "string",
    "is_correct": boolean
}
```
Saves user feedback about predictions.

## Model Architecture

The model uses a ResNet18 architecture with transfer learning:
- Base: Pre-trained ResNet18
- Fine-tuning: Custom fully connected layer for crop disease classification
- Input: 224x224 RGB images
- Output: Probability distribution over disease classes

## Configuration

### Training Configuration (`model/config.py`)

- `BATCH_SIZE`: Batch size for training (default: 32)
- `NUM_EPOCHS`: Number of training epochs (default: 20)
- `LEARNING_RATE`: Initial learning rate (default: 0.001)
- `IMAGE_SIZE`: Input image size (default: 224)

### Backend Configuration

Update `API_BASE_URL` in `frontend/app.js` if running on a different port or host.

## Logging

- **Predictions Log** (`logs/predictions.csv`): Records all disease predictions with timestamps and confidence scores
- **Feedback Log** (`logs/feedback.csv`): Stores user feedback for model improvement

## Troubleshooting

### Model File Not Found
- Ensure the model has been trained and saved to `model/saved_models/best_model.pth`
- Check that `class_indices.json` exists in the same directory

### API Connection Error
- Verify the backend server is running on port 5000
- Check `API_BASE_URL` in `frontend/app.js` matches your server address
- Ensure CORS is properly configured in the backend

### Image Upload Issues
- Check file size (must be < 10MB)
- Verify image format (PNG, JPG, JPEG supported)
- Ensure the image file is valid and not corrupted

## Future Enhancements

- [ ] Support for more crop types
- [ ] Real-time camera capture for mobile devices
- [ ] Multi-language support
- [ ] Advanced treatment recommendations based on region
- [ ] Model retraining pipeline with user feedback
- [ ] Admin dashboard for monitoring predictions

## License

This project is open source and available for educational purposes.

## Contributors

- Initial development and structure

## Acknowledgments

- New Plant Diseases Dataset
- PyTorch and torchvision libraries
- Flask framework
- Plant disease research community

