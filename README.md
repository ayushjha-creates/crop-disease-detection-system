# 🌾 Crop Disease Detection System

An intelligent crop disease detection system using deep learning with a web-based interface for farmers and agricultural professionals.

## 📋 Features

- 🤖 **AI-Powered Detection**: ResNet18-based model for accurate disease classification
- 🌐 **Web Interface**: User-friendly frontend for image upload and results
- 🐳 **Docker Ready**: Fully containerized for easy deployment
- 📊 **Real-time Results**: Fast predictions with confidence scores
- 💡 **Smart Recommendations**: Agricultural advice for detected diseases
- 🔄 **40 Disease Classes**: Covers multiple crops and disease types

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ayushjha-creates/crop-disease-detection-system.git
cd crop-disease-detection-system

# Configure environment
cp config.env.example .env
# Edit .env with your settings if needed

# Start the application
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:8080
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
# Serve the frontend (simple HTTP server)
cd frontend
python -m http.server 8080
# Or use any static file server
```

## 📁 Project Structure

```
crop-disease-detection-system/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main API application
│   ├── model_loader.py     # Model loading utilities
│   ├── recommendation_engine.py # Disease recommendations
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # Web interface
│   ├── index.html         # Main web page
│   ├── app.js             # Frontend JavaScript
│   └── style.css          # Styling
├── model/                  # ML model and training
│   ├── train_model.py     # Training script
│   ├── dataset_loader.py  # Data loading utilities
│   ├── saved_models/      # Trained model weights
│   └── data/              # Dataset (train/valid/test)
├── docker-compose.yml      # Multi-container setup
├── .dockerignore           # Docker ignore rules
└── config.env.example      # Environment variables template
```

## 🧬 Model Details

### Architecture
- **Base Model**: ResNet18 (pre-trained on ImageNet)
- **Fine-tuned**: For crop disease classification
- **Classes**: 38 different disease categories across multiple crops
- **Input**: RGB images (224x224 pixels)

### Supported Crops & Diseases
- **Apple**: Scab, Black Rot, Cedar Rust, Healthy
- **Cherry**: Powdery Mildew, Healthy
- **Corn**: Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
- **Grape**: Black Rot, Esca, Leaf Blight, Healthy
- **Peach**: Bacterial Spot, Healthy
- **Pepper**: Bacterial Spot, Healthy
- **Strawberry**: Leaf Scorch, Healthy
- **Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, 
  Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Healthy

### Performance
- **Training Accuracy**: ~95%+
- **Validation Accuracy**: ~92%+
- **Inference Time**: < 1 second per image

## 📊 API Documentation

### Main Endpoints

#### `POST /predict`
Upload an image for disease prediction.

**Request:**
```
Content-Type: multipart/form-data
file: <image_file>
```

**Response:**
```json
{
  "predicted_class": "Tomato___Early_blight",
  "confidence": 0.9234,
  "crop_name": "Tomato",
  "disease_name": "Early_blight",
  "recommendation": "Apply copper-based fungicides and remove affected leaves..."
}
```

#### `GET /`
Health check endpoint.

**Response:**
```json
{"message": "API running"}
```

### Interactive Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## 🛠️ Development

### Training the Model

```bash
cd model
python train_model.py
```

The training script will:
- Load the dataset from `model/data/`
- Train for 10 epochs with data augmentation
- Save the best model to `model/saved_models/`
- Generate training/validation accuracy metrics

### Model Retraining
To retrain with new data:
1. Add new images to `model/data/train/`, `model/data/valid/`, `model/data/test/`
2. Update class mappings if needed
3. Run the training script
4. Update the model files in the container

## 🐳 Docker Configuration

### Services
- **backend**: FastAPI application (port 8000)
- **frontend**: Static file server (port 8080)

### Building Images
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
```

### Production Deployment
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file from `config.env.example`:

```bash
# Model Configuration
MODEL_PATH=/app/model/saved_models/best_model.pth
CLASS_INDICES_PATH=/app/model/saved_models/class_indices.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
FRONTEND_PORT=8080
```

## 🌐 Deployment Options

### Render
1. Connect GitHub repository
2. Use `docker-compose.yml` for web service
3. Set environment variables
4. Deploy

### Netlify (Frontend Only)
1. Connect GitHub repository  
2. Set build directory to `frontend/`
3. Deploy static site

### AWS ECS
```bash
# Build and push to ECR
docker buildx build --platform linux/amd64 -t your-registry/crop-disease-backend .
docker push your-registry/crop-disease-backend

# Deploy to ECS using task definition
```

## 📈 Monitoring & Logging

### Health Checks
- Backend: `GET /` 
- Container health checks in docker-compose

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset: [Plant Village Dataset](https://plantvillage.org/)
- Model Architecture: [ResNet](https://arxiv.org/abs/1512.03385) by Microsoft Research
- Framework: [PyTorch](https://pytorch.org/)
- API: [FastAPI](https://fastapi.tiangolo.com/)

## 📞 Support

For questions and support:
- Create an [Issue](https://github.com/ayushjha-creates/crop-disease-detection-system/issues)
- Check the [Documentation](https://github.com/ayushjha-creates/crop-disease-detection-system/wiki)

---

⚡ **Built with ❤️ for farmers and agricultural advancement**