# Quick Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create models directory (if it doesn't exist)
mkdir -p ../models
```

## Step 2: Model Setup

**Option A: Train Your Own Model**

1. Download a dataset (CelebA-Spoof, CASIA-FASD, or Replay-Attack)
2. Organize into `datasets/real/` and `datasets/spoof/`
3. Train the model:
   ```bash
   cd backend
   python model/train_model.py
   ```

**Option B: Use Without Trained Model (Heuristic Mode)**

The system will work with basic heuristics if no model is found. However, accuracy will be limited. A trained model is recommended for production use.

## Step 3: Start Backend

```bash
cd backend
python main.py
```

Backend runs on `http://localhost:8000`

## Step 4: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on `http://localhost:3000`

## Testing

1. Open `http://localhost:3000` in your browser
2. Allow camera permissions when prompted
3. Click "Start Detection"
4. Point camera at your face
5. View real-time detection results

## Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS in production (required for camera access)
- Check browser permissions

### Model Not Found
- The system will use heuristic detection
- Train a model using `python backend/model/train_model.py`

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- In production, use `wss://` instead of `ws://`

