# Crop Disease Detection System

An AI-powered web application that identifies crop diseases from leaf images and provides treatment recommendations.

## What It Does

- Upload a photo of a crop leaf
- Get instant disease detection with confidence scores  
- Receive organic and chemical treatment options
- Learn preventive measures for future crops

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- 
###  Tech Stack
- **Backend**: FastAPI (Python) - speedy and light
- **Frontend**: Vanilla JavaScript + HTML/CSS - no heavy frameworks needed  
- **Model**: PyTorch ResNet18 - trained on crop diseases
- **Deployment**: Docker ready + simple Python HTTP server
- **Image Magic**: PIL for processing, NumPy for number crunching


### Installation

1. Clone the repository:
```bash
git clone https://github.com/ayushjha-creates/crop-disease-detection-system.git
cd crop-disease-detection-system
```

2. Set up virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

### Running the Application

**Easy Way (Recommended):**
```bash
./start_project.sh
```

**Manual Way:**

1. Start the backend server:
```bash
source .venv/bin/activate
cd backend
python server.py
```

2. In a new terminal, start the frontend:
```bash
cd frontend
python -m http.server 8080
```

3. Open your browser and go to: `http://localhost:8080`

### Stop the Application
```bash
./stop_servers.sh
```
## How to Use

1. Open the web interface at `http://localhost:8080`
2. Click "Choose File" or drag and drop a leaf image
3. Click "Analyze Disease" 
4. Wait a few seconds for results
5. View disease information and treatment recommendations

## Supported Formats
- JPG, JPEG, PNG, BMP
- Max file size: 10MB

## What the System Detects

The model can identify diseases in various crops including:
- Apple (Apple scab)
- Potato (Early blight, Late blight) 
- Tomato (Late blight, Leaf mold, Septoria leaf spot)
- Corn (Common rust)
- Squash (Powdery mildew)

And more - with confidence scores for each prediction.

## Docker Deployment

For production deployment:

```bash
docker-compose up -d
```

This will start both backend (port 8000) and frontend (port 8080) in containers.

## API Endpoints

If you want to use the backend directly:

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Upload image for prediction

Example curl request:
```bash
curl -X POST -F "file=@leaf_image.jpg" http://localhost:8000/predict
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## NOTE
Build with pytorch, ResNet18, a lot of coffee and a genuine desire to help plants live their best lives.
