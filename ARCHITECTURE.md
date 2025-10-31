# System Architecture

## Overview

The Face Liveness Detection System is a full-stack application that performs real-time detection of face spoofing attempts using computer vision and deep learning.

## Architecture Diagram

```
┌─────────────────┐
│   React Client  │
│  (Frontend)     │
│                 │
│  - Webcam       │◄────────┐
│  - WebSocket    │         │
│  - UI           │         │
└────────┬────────┘         │
         │                  │
         │ WebSocket        │ HTTP
         │ (Frames)         │ (Config)
         │                  │
         ▼                  │
┌─────────────────┐         │
│  FastAPI Server │         │
│   (Backend)     │         │
│                 │         │
│  - WebSocket    │         │
│  - Face Detect  │         │
│  - Inference    │         │
│  - Logging      │         │
└────────┬────────┘         │
         │                  │
         ├──────────────────┘
         │
         ▼
┌─────────────────┐
│   Components    │
│                 │
│  - MediaPipe    │
│  - OpenCV       │
│  - TensorFlow   │
│  - SQLite       │
└─────────────────┘
```

## Component Details

### Frontend (React)

**Location**: `frontend/src/`

**Key Components**:
1. **App.js**: Main application component
   - Manages active check toggle
   - Wraps FaceDetectionView

2. **FaceDetectionView.js**: Core detection component
   - Webcam capture using `react-webcam`
   - WebSocket client for real-time communication
   - Frame extraction and transmission
   - Result visualization

**Data Flow**:
```
Webcam → Frame Capture → Base64 Encode → WebSocket Send
                                                      ↓
Result Display ← JSON Parse ← WebSocket Receive ← Backend
```

### Backend (FastAPI)

**Location**: `backend/`

**Main Components**:

1. **main.py**: FastAPI application
   - WebSocket endpoint (`/ws`) for frame streaming
   - HTTP endpoints for health checks and configuration
   - CORS middleware for frontend communication

2. **utils/face_detector.py**: Face detection utilities
   - MediaPipe face detection
   - Face ROI extraction
   - Blink detection (eye aspect ratio)
   - Head movement tracking

3. **utils/liveness_detector.py**: Liveness detection engine
   - MobileNetV2 model loading and inference
   - Passive liveness check (CNN-based)
   - Active liveness check (user interaction)
   - Confidence scoring

4. **utils/database.py**: Inference logging
   - SQLite database operations
   - Store detection results
   - Retrieve historical logs

**Data Flow**:
```
WebSocket Receive → Base64 Decode → Face Detection → ROI Extraction
                                                          ↓
Result ← JSON Encode ← Log Inference ← Liveness Detection ← Preprocess
```

## Detection Pipeline

### Passive Detection Flow

```
1. Frame received from client
2. Face detection (MediaPipe)
3. Extract face ROI (128×128)
4. Preprocess (normalize [0,1])
5. CNN inference (MobileNetV2)
6. Output: is_real, confidence
```

### Active Detection Flow

```
1. Passive detection result
2. Monitor facial landmarks
3. Blink detection (EAR threshold)
4. Head movement detection
5. Both must pass for "Real"
```

## Model Architecture

### MobileNetV2-Based CNN

```
Input: 128×128×3 RGB image
       ↓
MobileNetV2 Base (frozen, ImageNet weights)
       ↓
GlobalAveragePooling2D
       ↓
Dense(128, ReLU) + Dropout(0.5)
       ↓
Dense(64, ReLU) + Dropout(0.3)
       ↓
Dense(1, Sigmoid)
       ↓
Output: [0, 1] (probability of being real)
```

**Training**:
- Loss: Binary cross-entropy
- Optimizer: Adam (lr=0.001)
- Metrics: Accuracy, Precision, Recall
- Augmentation: Rotation, shift, zoom, flip

## WebSocket Protocol

### Client → Server

**Frame Message**:
```json
{
  "type": "frame",
  "data": "base64_encoded_jpeg_image"
}
```

**Control Messages**:
```json
{
  "type": "ping"  // Heartbeat
}
```

```json
{
  "type": "reset_active_check"
}
```

### Server → Client

**Result Message**:
```json
{
  "type": "result",
  "face_detected": true,
  "is_real": true,
  "confidence": 0.95,
  "active_check_passed": true,
  "active_check_message": "Active check passed",
  "bbox": [100, 150, 200, 250]
}
```

**Error Message**:
```json
{
  "type": "error",
  "message": "Error description"
}
```

## Database Schema

**Table: inference_logs**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | DATETIME | Detection timestamp |
| is_real | BOOLEAN | Detection result |
| confidence | REAL | Confidence score |
| active_check_passed | BOOLEAN | Active check status |
| active_check_message | TEXT | Active check message |
| frame_data | BLOB | Thumbnail image |
| metadata | TEXT | JSON metadata |

## Key Algorithms

### Blink Detection

Uses Eye Aspect Ratio (EAR):
```
EAR = (|p2 - p6| + |p3 - p5|) / (2 * |p1 - p4|)

Where p1-p6 are eye landmark points
```

**Threshold**: EAR < 0.25 indicates closed eye/blink

### Head Movement Detection

Tracks nose tip position:
```
movement = sqrt((x_new - x_old)² + (y_new - y_old)²)
```

**Threshold**: movement > 0.02 indicates significant head turn

### Passive Detection Heuristic (Fallback)

When model not available:
```
Laplacian Variance = variance of Laplacian operator on grayscale face

Threshold: variance > 100 (real faces have more texture)
```

## Performance Considerations

### Frame Rate
- Client sends frames at ~10 FPS (100ms interval)
- Backend processes frames asynchronously
- WebSocket keeps connection alive with heartbeats

### Model Inference
- MobileNetV2 is lightweight (~14M parameters)
- Inference time: ~10-50ms on CPU
- Can be optimized with TensorFlow Lite for mobile

### Resource Usage
- Memory: ~200-500MB (model + buffers)
- CPU: Moderate (depends on frame rate)
- GPU: Optional (TensorFlow can use GPU if available)

## Security Considerations

1. **CORS**: Configured for specific origins in production
2. **WebSocket**: Secure (WSS) in production
3. **Input Validation**: Base64 decoding with error handling
4. **Rate Limiting**: Should be added for production
5. **Authentication**: Not included (add if needed)

## Extension Points

1. **Additional Active Checks**:
   - Smile detection
   - Mouth movement
   - Eye gaze direction

2. **Model Improvements**:
   - Fine-tuning with domain-specific data
   - Ensemble models
   - Temporal analysis (video sequences)

3. **Features**:
   - User authentication
   - Multi-user support
   - Analytics dashboard
   - Real-time alerts

4. **Optimization**:
   - Model quantization
   - Edge deployment (mobile)
   - Batch processing
   - Caching strategies

