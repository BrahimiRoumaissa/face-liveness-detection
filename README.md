# Face Liveness Detection System

A full-stack real-time face liveness detection system that can distinguish between real faces and spoofs (photos, videos, or deepfakes) using computer vision and deep learning.

## 🎯 Features

- **Real-time Face Detection**: Uses OpenCV + MediaPipe for robust face detection and alignment
- **Two-Stage Liveness Detection**:
  - **Passive Check**: CNN-based analysis of texture, color, and depth cues
  - **Active Check**: Requires user interaction (blink, head movement)
- **MobileNetV2 CNN Model**: Lightweight binary classification model (real vs spoof)
- **WebSocket Streaming**: Real-time frame streaming and inference via WebSocket
- **Database Logging**: SQLite database for storing inference logs
- **Modern UI**: Beautiful React frontend with real-time visualization

## 🏗️ Project Structure

```
project/
├── backend/
│   ├── main.py                 # FastAPI server with WebSocket
│   ├── model/
│   │   ├── train_model.py      # Model training script
│   │   └── preprocess_dataset.py
│   ├── utils/
│   │   ├── face_detector.py    # OpenCV + MediaPipe face detection
│   │   ├── liveness_detector.py # MobileNetV2 liveness detection
│   │   └── database.py         # SQLite inference logging
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   └── FaceDetectionView.js
│   │   └── index.js
│   └── package.json
├── models/                     # Trained model directory
├── datasets/                   # Dataset directory
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train or download model**:
   
   **Option A: Train your own model** (requires dataset):
   ```bash
   # Organize dataset into datasets/real/ and datasets/spoof/
   python model/train_model.py
   ```
   
   **Option B: Use pre-trained model** (download from [releases](https://github.com/your-repo/releases) or train with provided dataset links)
   
   Place the model at `models/liveness_model.h5`

5. **Start the backend server**:
   ```bash
   python main.py
   # Or: uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create `.env` file** (optional, defaults to localhost):
   ```env
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_WS_URL=ws://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```
   
   Frontend will run on `http://localhost:3000`

## 📊 Dataset

### Recommended Datasets

1. **CelebA-Spoof**: https://mmlab.ie.cuhk.edu.hk/projects/CelebA_Spoof.html
2. **CASIA-FASD**: http://www.cbsr.ia.ac.cn/english/CASIA-FASD.asp
3. **Replay-Attack**: https://www.idiap.ch/en/dataset/replayattack

### Dataset Preparation

Organize your dataset in the following structure:
```
datasets/
├── real/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── spoof/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

### Training the Model

```bash
cd backend
python model/train_model.py
```

The script will:
- Load images from `datasets/`
- Preprocess (resize to 128×128, normalize)
- Split into train/val/test (70/20/10)
- Train MobileNetV2-based model
- Save model to `models/liveness_model.h5`

Training parameters can be adjusted in `train_model.py`:
- `epochs`: Number of training epochs (default: 10)
- `batch_size`: Batch size (default: 32)
- `validation_split`: Validation split ratio (default: 0.2)

## 🔧 Key Components

### Backend

#### 1. Face Detector (`utils/face_detector.py`)
- **MediaPipe Face Detection**: Detects faces in frames
- **Face Alignment**: Extracts face ROI (128×128)
- **Blink Detection**: Analyzes eye aspect ratio (EAR)
- **Head Movement Detection**: Tracks facial landmarks

#### 2. Liveness Detector (`utils/liveness_detector.py`)
- **Passive Check**: CNN inference on face ROI
- **Active Check**: Monitors user interactions
- **Confidence Scoring**: Returns detection confidence

#### 3. WebSocket Server (`main.py`)
- Real-time frame streaming
- Inference pipeline
- Result broadcasting

### Frontend

#### FaceDetectionView Component
- **Webcam Capture**: `react-webcam` for video stream
- **WebSocket Client**: Sends frames to backend
- **Real-time Visualization**: Shows detection results with bounding box
- **UI Indicators**: Green (real) / Red (spoof)

## 🌐 API Endpoints

### HTTP Endpoints

- `GET /` - Health check
- `GET /health` - Server health and model status
- `POST /toggle-active-check` - Toggle active liveness check
- `GET /logs` - Get recent inference logs

### WebSocket Endpoint

- `ws://localhost:8000/ws` - Real-time frame streaming

**Message Format**:
```json
{
  "type": "frame",
  "data": "base64_encoded_image"
}
```

**Response Format**:
```json
{
  "type": "result",
  "face_detected": true,
  "is_real": true,
  "confidence": 0.95,
  "active_check_passed": true,
  "active_check_message": "Active check passed",
  "bbox": [x, y, width, height]
}
```

## 🚢 Deployment

### Backend (Render/Railway)

1. **Prepare for deployment**:
   ```bash
   cd backend
   # Ensure requirements.txt is up to date
   ```

2. **Deploy to Render**:
   - Create new Web Service
   - Connect your repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables if needed

3. **Deploy to Railway**:
   - Create new project
   - Connect repository
   - Railway auto-detects Python and installs requirements
   - Add `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. **Build frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**:
   - Install Vercel CLI: `npm i -g vercel`
   - Run: `vercel`
   - Update `.env` with production backend URL:
     ```
     REACT_APP_API_URL=https://your-backend.railway.app
     REACT_APP_WS_URL=wss://your-backend.railway.app
     ```

3. **Configure WebSocket**:
   - Ensure WebSocket support in your hosting (Render/Railway support WebSockets)
   - Use `wss://` for secure WebSocket in production

## 📝 Usage

1. **Start Backend**: Run `python backend/main.py`
2. **Start Frontend**: Run `npm start` in frontend directory
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Click "Start Detection"**: Allow camera permissions
5. **View Results**: See real-time liveness detection results

### Active Check Mode

Toggle active check to enable two-stage verification:
- **Passive**: CNN-based detection
- **Active**: User must blink and turn head

## 🛠️ Troubleshooting

### Model Not Loading
- Ensure `models/liveness_model.h5` exists
- Check file path in `liveness_detector.py`
- Verify model is trained and saved correctly

### WebSocket Connection Issues
- Check backend is running on correct port
- Verify CORS settings in `main.py`
- Use `wss://` in production (HTTPS required)

### Camera Permissions
- Allow browser camera access
- Check HTTPS in production (required for camera)

### Performance Issues
- Reduce frame rate (adjust interval in `FaceDetectionView.js`)
- Use smaller input resolution
- Optimize model (quantization, pruning)

## 📚 Technical Details

### Model Architecture

```
MobileNetV2 (base, frozen)
    ↓
GlobalAveragePooling2D
    ↓
Dense(128, ReLU) + Dropout(0.5)
    ↓
Dense(64, ReLU) + Dropout(0.3)
    ↓
Dense(1, Sigmoid) → Binary Classification
```

### Detection Pipeline

1. **Frame Capture** → Webcam stream
2. **Face Detection** → MediaPipe face detection
3. **Face Extraction** → Crop and resize to 128×128
4. **Preprocessing** → Normalize [0, 1]
5. **Inference** → MobileNetV2 prediction
6. **Active Check** (optional) → Blink/head movement
7. **Result** → Real/Spoof with confidence

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a prototype system. For production use, consider:
- Using larger, more diverse datasets
- Implementing additional security measures
- Fine-tuning model hyperparameters
- Adding authentication and rate limiting
- Implementing proper error handling and logging
