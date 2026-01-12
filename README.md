# Crop Disease Detection

I built this project to help farmers quickly identify plant diseases using AI. Upload a photo of a plant leaf, and the system will tell you what's wrong and how to fix it.

## What It Does

- **Takes plant photos** and tells you if there's a disease
- **Shows confidence scores** so you know how sure the AI is
- **Gives practical advice** for treating each specific disease
- **Works with 40+ disease types** across 8 different crops
- **Runs in your browser** - no software needed

## Quick Start (Docker)

```bash
# Clone it
git clone https://github.com/ayushjha-creates/crop-disease-detection-system.git
cd crop-disease-detection-system

# Set it up
cp config.env.example .env

# Run it
docker-compose up --build
```

Now open your browser to:
- **Frontend**: http://localhost:8080
- **API docs**: http://localhost:8000/docs

## Manual Setup (No Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
python -m http.server 8080
```

## How It's Organized

```
crop-disease-detection-system/
├── backend/          # The AI API (FastAPI)
├── frontend/         # The web interface
├── model/            # Training code and data
├── docker-compose.yml # Docker setup
└── README.md         # This file
```

## The AI Model

I used a ResNet18 model (pre-trained on ImageNet) and fine-tuned it on plant disease images. It can identify:

**Crops covered:**
- Apple, Cherry, Corn, Grape, Peach, Pepper, Strawberry, Tomato

**Diseases it catches:**
- Common ones like Early Blight, Powdery Mildew, Black Rot
- Plus "healthy" when there's nothing wrong

**How well it works:**
- Training accuracy: ~95%
- Validation accuracy: ~92%
- Takes less than 1 second per image

## Using the API

The main endpoint is `POST /predict`. Upload a leaf photo and get back:

```json
{
  "predicted_class": "Tomato___Early_blight",
  "confidence": 0.92,
  "crop_name": "Tomato", 
  "disease_name": "Early_blight",
  "recommendation": "Remove affected leaves, apply copper fungicide..."
}
```

For full API docs: http://localhost:8000/docs

## Training Your Own Model

If you want to retrain with your own data:

```bash
cd model
python train_model.py
```

The script handles:
- Loading images from `model/data/`
- Data augmentation (flips, rotations, etc.)
- Saving the best model automatically

## Docker Details

The setup includes two containers:
- **backend**: FastAPI server on port 8000
- **frontend**: Simple web server on port 8080

## Deployment Options

**Render:** Just connect your GitHub repo and it'll build automatically.

**Netlify:** Works great for just the frontend.

**Any cloud provider:** The Docker setup works anywhere.

## Troubleshooting

**If the model won't load:**
- Check that `model/saved_models/best_model.pth` exists
- Make sure the paths in `config.env` are correct

**If the frontend can't reach the API:**
- Verify both services are running
- Check the API URL in `frontend/app.js`

**Training issues:**
- Make sure your dataset follows the structure: `data/train/class_name/images`

## Contributing

Found a bug or want to add a feature?

1. Fork this repo
2. Make your changes
3. Open a pull request

I'm especially interested in:
- More disease types
- Better recommendations
- Mobile app ideas
- Real-world testing feedback

## Why I Built This

As someone interested in both AI and agriculture, I wanted to create something practical that could actually help farmers. Many small-scale farmers can't afford expensive disease diagnosis tools, but most have smartphones. This project is my attempt to bridge that gap.

The model isn't perfect, but it's getting better. I trained it on the Plant Village dataset and am working on adding more diseases and improving the recommendations.

## Got Questions?

- **Open an issue** for bugs or feature requests
- **Check the code** - it's all open source
- **Test it out** and let me know how it works on your plants!

---

*Built with Python, PyTorch, FastAPI, and way too much coffee*