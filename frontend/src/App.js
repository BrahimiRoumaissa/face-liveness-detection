import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import './App.css';
import FaceDetectionView from './components/FaceDetectionView';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [activeCheckEnabled, setActiveCheckEnabled] = useState(false);

  const toggleActiveCheck = async () => {
    try {
      const response = await fetch(`${API_URL}/toggle-active-check`, {
        method: 'POST',
      });
      const data = await response.json();
      setActiveCheckEnabled(data.active_check_enabled);
    } catch (error) {
      console.error('Error toggling active check:', error);
    }
  };

  useEffect(() => {
    // Fetch initial active check state
    fetch(`${API_URL}/toggle-active-check`, { method: 'POST' })
      .then(res => res.json())
      .then(data => setActiveCheckEnabled(data.active_check_enabled))
      .catch(console.error);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Face Liveness Detection System</h1>
        <p className="subtitle">Detect if a person is real or a spoof in real-time</p>
      </header>

      <main className="App-main">
        <div className="controls">
          <button
            className={`toggle-btn ${activeCheckEnabled ? 'active' : ''}`}
            onClick={toggleActiveCheck}
          >
            {activeCheckEnabled ? '✓ Active Check Enabled' : 'Active Check Disabled'}
          </button>
          <span className="info-text">
            {activeCheckEnabled
              ? 'User must blink and turn head'
              : 'Passive detection only'}
          </span>
        </div>

        <FaceDetectionView
          isDetecting={isDetecting}
          setIsDetecting={setIsDetecting}
          activeCheckEnabled={activeCheckEnabled}
        />
      </main>

      <footer className="App-footer">
        <p>Powered by OpenCV, MediaPipe, and TensorFlow</p>
      </footer>
    </div>
  );
}

export default App;

