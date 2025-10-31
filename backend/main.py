"""
FastAPI Backend for Face Liveness Detection System
"""
import base64
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from typing import Optional

from utils.face_detector import FaceDetector
from utils.liveness_detector import LivenessDetector
from utils.database import InferenceLogger

app = FastAPI(title="Face Liveness Detection API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
face_detector = FaceDetector()
liveness_detector = LivenessDetector()
inference_logger = InferenceLogger()

# Active check mode flag
active_check_enabled = False


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Face Liveness Detection API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": liveness_detector.model is not None}


@app.post("/toggle-active-check")
async def toggle_active_check():
    """Toggle active liveness check mode"""
    global active_check_enabled
    active_check_enabled = not active_check_enabled
    
    if active_check_enabled:
        liveness_detector.reset_active_check()
    
    return {
        "active_check_enabled": active_check_enabled,
        "message": "Active check enabled" if active_check_enabled else "Active check disabled"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time frame streaming and inference
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive frame data from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "frame":
                # Decode base64 image
                image_data = base64.b64decode(message["data"])
                nparr = np.frombuffer(image_data, dtype=np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to decode frame"
                    })
                    continue
                
                # Detect face
                bbox = face_detector.detect_face(frame)
                
                if bbox is None:
                    await websocket.send_json({
                        "type": "result",
                        "face_detected": False,
                        "message": "No face detected"
                    })
                    continue
                
                # Extract face ROI
                face_roi = face_detector.extract_face_roi(frame, bbox)
                
                if face_roi is None:
                    await websocket.send_json({
                        "type": "result",
                        "face_detected": False,
                        "message": "Failed to extract face"
                    })
                    continue
                
                # Perform liveness detection
                result = liveness_detector.detect(
                    face_roi,
                    frame=frame if active_check_enabled else None,
                    face_detector=face_detector if active_check_enabled else None,
                    use_active_check=active_check_enabled
                )
                
                # Log inference (store small thumbnail)
                _, buffer = cv2.imencode('.jpg', face_roi, [cv2.IMWRITE_JPEG_QUALITY, 50])
                thumbnail_bytes = buffer.tobytes()
                
                inference_logger.log_inference(
                    result,
                    frame_data=thumbnail_bytes,
                    metadata={
                        "bbox": bbox,
                        "active_check_enabled": active_check_enabled
                    }
                )
                
                # Send result back to client
                await websocket.send_json({
                    "type": "result",
                    "face_detected": True,
                    "is_real": result["is_real"],
                    "confidence": round(result["confidence"], 3),
                    "active_check_passed": result.get("active_check_passed", True),
                    "active_check_message": result.get("active_check_message", ""),
                    "bbox": bbox
                })
            
            elif message["type"] == "ping":
                # Heartbeat
                await websocket.send_json({"type": "pong"})
            
            elif message["type"] == "reset_active_check":
                # Reset active check state
                liveness_detector.reset_active_check()
                await websocket.send_json({
                    "type": "active_check_reset",
                    "message": "Active check reset"
                })
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })


@app.get("/logs")
async def get_logs(limit: int = 100):
    """Get recent inference logs"""
    logs = inference_logger.get_recent_logs(limit=limit)
    return {"logs": logs, "count": len(logs)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
