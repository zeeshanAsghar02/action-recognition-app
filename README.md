# 🎬 Action Recognition Web Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A modern full-stack web application for recognizing human actions in images using deep learning**

**Deep Learning Assignment 04 - Muhammad Zeeshan (221360)**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## 🎓 Assignment Overview

This project fulfills the requirements of the Deep Learning course assignment:

✅ **CNN + LSTM Models** - Hybrid architecture for action recognition  
✅ **Image Annotation** - Recognizes and labels actions in images  
✅ **Frontend Integration** - Modern web interface for easy interaction  
✅ **GitHub Deployment** - Complete codebase with documentation  
✅ **Sample Images** - Test images provided in `sample_images/` folder  
✅ **REST API** - FastAPI-based communication between frontend and model  
✅ **40 Action Classes** - Trained on comprehensive action dataset  

---

## 📖 Overview

This project implements a complete **Action Recognition System** that predicts human actions from images using a hybrid **CNN-LSTM** deep learning model. The application features a professional FastAPI backend and a modern, responsive frontend interface.

### 🎯 Key Highlights

- **40 Action Classes** - Recognizes diverse human activities from images
- **Hybrid Architecture** - ResNet50 (CNN) + LSTM for robust feature extraction
- **REST API** - FastAPI backend with automatic Swagger documentation
- **Modern UI** - Responsive, animated frontend with real-time predictions
- **Production Ready** - Error handling, logging, and deployment-ready code

---

## ✨ Features

### Backend
✅ FastAPI REST API with automatic documentation  
✅ Pre-trained PyTorch CNN-LSTM model  
✅ Image preprocessing with ImageNet normalization  
✅ Efficient singleton pattern for model loading  
✅ CORS support for cross-origin requests  
✅ Comprehensive error handling and logging  
✅ Automatic temporary file cleanup  

### Frontend
✅ Modern, responsive UI design  
✅ JPG/JPEG image upload support  
✅ Real-time prediction display  
✅ Confidence visualization with animated progress bars  
✅ Loading states and smooth animations  
✅ User-friendly error messages  
✅ Display of all 40 supported action classes  

---

## 🎬 Demo

### Screenshots

**Main Interface**
```
┌─────────────────────────────────────┐
│  🎬 Action Recognition              │
│  Upload an image to predict action  │
│                                     │
│  [📤 Click to upload image]         │
│     JPG/JPEG only (max 10MB)        │
│                                     │
│  📋 Supported Actions (40 Classes)  │
│  ┌──────────┬──────────┬────────┐  │
│  │ Action 1 │ Action 2 │ ...    │  │
│  └──────────┴──────────┴────────┘  │
└─────────────────────────────────────┘
```

**Prediction Result**
```
┌─────────────────────────────────────┐
│  ✅ Prediction Results               │
│                                     │
│  Predicted Action: Playing Guitar   │
│  Confidence: 95.23%                 │
│  ████████████████░░░░  95%          │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
action-recognition-app/
│
├── backend/                       # Backend API and ML model
│   ├── api.py                    # FastAPI application
│   ├── inference.py              # Model inference logic
│   ├── cnn_lstm_model.py         # Model architecture definition
│   ├── cnn_lstm_action_model.pth # Pre-trained model weights (97MB)
│   └── action_classes.json       # 40 action class labels
│
├── frontend/                      # Frontend web interface
│   ├── index.html                # Main HTML page
│   ├── app.js                    # JavaScript application logic
│   └── style.css                 # Styling and animations
│
├── .gitignore                     # Git ignore configuration
└── README.md                      # Project documentation
```

---

## 🔧 Prerequisites

Before running this application, ensure you have:

- **Python** 3.8 or higher
- **pip** package manager
- **Modern web browser** (Chrome, Firefox, Safari, or Edge)
- **Git** (for cloning the repository)

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/action-recognition-app.git
cd action-recognition-app
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install fastapi uvicorn python-multipart pillow torch torchvision
```

**Or use requirements.txt:**
```bash
pip install -r requirements.txt
```

**Required packages:**
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server for running FastAPI
- `python-multipart` - File upload handling
- `pillow` - Image processing library
- `torch` - PyTorch deep learning framework
- `torchvision` - Computer vision utilities and pre-trained models

### 4️⃣ Download Pre-trained Model

⚠️ **Important:** The model file is 110MB and not included in the repository due to GitHub's file size limits.

**Option 1: Use Your Trained Model**
- Place your trained `cnn_lstm_action_model.pth` file in the `backend/` folder

**Option 2: Contact for Model Access**
- The pre-trained model can be provided separately
- Contact: [Your Contact Information]

### 5️⃣ Verify Installation

```bash
python -c "import torch; import fastapi; print('✅ All dependencies installed successfully!')"
```

---

## 🚀 Usage

### Quick Start

**1. Start the Backend Server:**

```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Initializing Action Recognition model...
INFO:     Using device: cpu
INFO:     Loaded 40 action classes
INFO:     Model loaded successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend API: **http://localhost:8000**  
📚 Interactive API Docs: **http://localhost:8000/docs**

---

**2. Open the Frontend:**

Simply double-click `frontend/index.html` or run:

```bash
# Windows
start frontend\index.html

# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html
```

Alternatively, use a local server:

```bash
cd frontend
python -m http.server 8080
# Open http://localhost:8080 in your browser
```

---

### Using the Application

1. **Upload Image** - Click the upload button and select a JPG/JPEG image
2. **Preview** - View your uploaded image in the preview section
3. **Predict** - Click the "Predict Action" button
4. **View Results** - See the predicted action and confidence score
5. **Try Another** - Click the remove button (❌) and upload a new image

---

## 📚 API Documentation

### Interactive Documentation

Visit **http://localhost:8000/docs** for interactive Swagger UI documentation.

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Predict Action
```http
POST /predict
Content-Type: multipart/form-data
```

**Request:**
- `file`: Image file (JPG/JPEG)

**Response:**
```json
{
  "action": "playing_guitar",
  "confidence": 0.9523
}
```

### Example API Calls

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## 🎯 Supported Actions

The model recognizes **40 different human actions**:

<details>
<summary>📋 Click to view all 40 action classes</summary>

1. Applauding
2. Blowing Bubbles
3. Brushing Teeth
4. Cleaning The Floor
5. Climbing
6. Cooking
7. Cutting Trees
8. Cutting Vegetables
9. Drinking
10. Feeding A Horse
11. Fishing
12. Fixing A Bike
13. Fixing A Car
14. Gardening
15. Holding An Umbrella
16. Jumping
17. Looking Through A Microscope
18. Looking Through A Telescope
19. Phoning
20. Playing Guitar
21. Playing Violin
22. Pouring Liquid
23. Pushing A Cart
24. Reading
25. Riding A Bike
26. Riding A Horse
27. Rowing A Boat
28. Running
29. Shooting An Arrow
30. Smoking
31. Taking Photos
32. Texting Message
33. Throwing Frisby
34. Using A Computer
35. Walking The Dog
36. Washing Dishes
37. Watching TV
38. Waving Hands
39. Writing On A Board
40. Writing On A Book

</details>

---

## 🏗️ Model Architecture

### CNN-LSTM Hybrid Architecture

```
Input Image (224×224×3)
         ↓
    ResNet50 CNN
  (Feature Extractor)
         ↓
   2048-D Features
         ↓
      LSTM Layer
    (512 hidden units)
         ↓
  Fully Connected
         ↓
   40 Action Classes
```

**Components:**
- **CNN:** ResNet50 pre-trained on ImageNet
- **LSTM:** Single-layer LSTM with 512 hidden units
- **Classifier:** Fully connected layer outputting 40 classes

**Preprocessing:**
- Resize to 224×224 pixels
- Normalize with ImageNet mean/std:
  - Mean: [0.485, 0.456, 0.406]
  - Std: [0.229, 0.224, 0.225]

---

## 🌐 Deployment

### Deploying the Backend

#### Option 1: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/ /app/backend/
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 2: Cloud Platforms

- **Render**: Connect repository and deploy
- **Railway**: `railway init` → `railway up`
- **Heroku**: Add `Procfile` and deploy
- **AWS/GCP**: Deploy on EC2/Cloud Run

### Deploying the Frontend

- **GitHub Pages**: Push frontend folder to `gh-pages` branch
- **Netlify**: Drag and drop frontend folder
- **Vercel**: Import repository and set root directory

---

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Verify all dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

**Frontend can't connect:**
- Ensure backend is running on `http://localhost:8000`
- Check browser console (F12) for errors
- Verify CORS is enabled (already configured)

**Model not loading:**
- Ensure `cnn_lstm_action_model.pth` exists in `backend/` folder
- Ensure `action_classes.json` exists in `backend/` folder
- Check file paths are correct

**Low accuracy predictions:**
- Use high-quality, clear images
- Ensure the action is clearly visible
- Try images similar to training data

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Muhammad Zeeshan** (221360)  
Deep Learning Assignment 04

---

## 🙏 Acknowledgments

- PyTorch Team for the deep learning framework
- FastAPI for the modern web framework
- ResNet50 pre-trained model from torchvision
- Action recognition dataset contributors

---

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ using PyTorch and FastAPI

</div>
