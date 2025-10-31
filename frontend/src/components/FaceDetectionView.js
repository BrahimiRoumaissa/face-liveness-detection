import React, { useRef, useEffect, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import './FaceDetectionView.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

const FaceDetectionView = ({ isDetecting, setIsDetecting, activeCheckEnabled }) => {
  const webcamRef = useRef(null);
  const wsRef = useRef(null);
  const frameIntervalRef = useRef(null);
  const canvasRef = useRef(null);
  
  const [detectionResult, setDetectionResult] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [fps, setFps] = useState(0);
  const frameCountRef = useRef(0);
  const lastFpsUpdateRef = useRef(Date.now());

  // Connect to WebSocket
  const connectWebSocket = useCallback(() => {
    try {
      const ws = new WebSocket(`${WS_URL}/ws`);
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        setIsDetecting(true);
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'result') {
          setDetectionResult(data);
          drawBoundingBox(data.bbox);
        } else if (data.type === 'pong') {
          // Heartbeat response
        } else if (data.type === 'error') {
          console.error('WebSocket error:', data.message);
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('error');
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
        setIsDetecting(false);
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
      
      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      setConnectionStatus('error');
    }
  }, [setIsDetecting]);

  // Send frame to backend
  const sendFrame = useCallback(() => {
    if (webcamRef.current && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        // Convert data URL to base64
        const base64Data = imageSrc.split(',')[1];
        
        wsRef.current.send(JSON.stringify({
          type: 'frame',
          data: base64Data
        }));
        
        // Update FPS counter
        frameCountRef.current++;
        const now = Date.now();
        if (now - lastFpsUpdateRef.current >= 1000) {
          setFps(frameCountRef.current);
          frameCountRef.current = 0;
          lastFpsUpdateRef.current = now;
        }
      }
    }
  }, []);

  // Draw bounding box on canvas
  const drawBoundingBox = (bbox) => {
    const canvas = canvasRef.current;
    if (!canvas || !bbox) return;
    
    const video = webcamRef.current.video;
    if (!video) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw bounding box
    const [x, y, width, height] = bbox;
    ctx.strokeStyle = detectionResult?.is_real ? '#4caf50' : '#f44336';
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, width, height);
  };

  // Start/stop detection
  useEffect(() => {
    if (isDetecting) {
      connectWebSocket();
      
      // Send frames at ~10 FPS
      frameIntervalRef.current = setInterval(sendFrame, 100);
      
      return () => {
        if (frameIntervalRef.current) {
          clearInterval(frameIntervalRef.current);
        }
        if (wsRef.current) {
          wsRef.current.close();
        }
      };
    } else {
      if (frameIntervalRef.current) {
        clearInterval(frameIntervalRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    }
  }, [isDetecting, connectWebSocket, sendFrame]);

  const startDetection = () => {
    setIsDetecting(true);
  };

  const stopDetection = () => {
    setIsDetecting(false);
  };

  return (
    <div className="face-detection-view">
      <div className="webcam-container">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={{
            width: 640,
            height: 480,
            facingMode: "user"
          }}
          className="webcam"
        />
        <canvas
          ref={canvasRef}
          className="overlay-canvas"
        />
        
        {detectionResult && (
          <div className={`result-overlay ${detectionResult.is_real ? 'real' : 'spoof'}`}>
            <div className="result-indicator">
              <span className="result-icon">
                {detectionResult.is_real ? '✓' : '✗'}
              </span>
              <span className="result-text">
                {detectionResult.is_real ? 'REAL' : 'SPOOF'}
              </span>
            </div>
            <div className="confidence">
              Confidence: {(detectionResult.confidence * 100).toFixed(1)}%
            </div>
            {activeCheckEnabled && !detectionResult.active_check_passed && (
              <div className="active-check-message">
                {detectionResult.active_check_message}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="controls-panel">
        <button
          className={`detect-btn ${isDetecting ? 'stop' : 'start'}`}
          onClick={isDetecting ? stopDetection : startDetection}
        >
          {isDetecting ? 'Stop Detection' : 'Start Detection'}
        </button>
        
        <div className="status-info">
          <div className="status-item">
            <span className="status-label">Connection:</span>
            <span className={`status-value ${connectionStatus}`}>
              {connectionStatus.toUpperCase()}
            </span>
          </div>
          {isDetecting && (
            <div className="status-item">
              <span className="status-label">FPS:</span>
              <span className="status-value">{fps}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FaceDetectionView;

