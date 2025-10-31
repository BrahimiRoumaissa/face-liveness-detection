"""
Liveness Detection using MobileNetV2-based CNN
Implements passive and active liveness checks
"""
import cv2
import numpy as np
from tensorflow import keras


class LivenessDetector:
    def __init__(self, model_path="models/liveness_model.h5"):
        """
        Initialize liveness detector
        Args:
            model_path: Path to trained MobileNetV2 model
        """
        self.model = None
        self.model_path = model_path
        self.load_model()
        
        # Active liveness state
        self.active_check_state = {
            'blink_detected': False,
            'head_moved': False,
            'blink_count': 0,
            'previous_landmarks': None
        }
    
    def load_model(self):
        """Load the trained liveness detection model"""
        try:
            self.model = keras.models.load_model(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            print(f"Warning: Could not load model from {self.model_path}: {e}")
            print("Using default model initialization (requires training)")
            self.model = None
    
    def preprocess_frame(self, face_roi):
        """
        Preprocess face ROI for model input
        Args:
            face_roi: Face region (128x128x3)
        Returns: Preprocessed array
        """
        if face_roi is None:
            return None
        
        # Resize if needed
        if face_roi.shape[:2] != (128, 128):
            face_roi = cv2.resize(face_roi, (128, 128))
        
        # Convert BGR to RGB
        face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        face_normalized = face_rgb.astype(np.float32) / 255.0
        
        # Add batch dimension
        face_batch = np.expand_dims(face_normalized, axis=0)
        
        return face_batch
    
    def passive_check(self, face_roi):
        """
        Passive liveness check: Analyze texture, color, and depth cues using CNN
        Args:
            face_roi: Face region of interest
        Returns: (is_real: bool, confidence: float)
        """
        if self.model is None:
            # Fallback: simple heuristic if model not loaded
            return self._heuristic_check(face_roi), 0.5
        
        preprocessed = self.preprocess_frame(face_roi)
        if preprocessed is None:
            return False, 0.0
        
        # Predict
        prediction = self.model.predict(preprocessed, verbose=0)[0][0]
        
        # prediction > 0.5 means real, < 0.5 means spoof
        is_real = prediction > 0.5
        confidence = prediction if is_real else 1.0 - prediction
        
        return is_real, float(confidence)
    
    def _heuristic_check(self, face_roi):
        """
        Simple heuristic check when model is not available
        Analyzes basic image properties
        """
        if face_roi is None:
            return False
        
        # Convert to grayscale
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance (measures image sharpness)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Real faces typically have higher variance (more texture)
        # Threshold can be adjusted based on testing
        return laplacian_var > 100
    
    def active_check(self, frame, face_detector):
        """
        Active liveness check: Require user actions (blink, head movement)
        Args:
            frame: Current frame
            face_detector: FaceDetector instance
        Returns: (passed: bool, status_message: str)
        """
        state = self.active_check_state
        
        # Check for blink
        if face_detector.detect_blink(frame):
            if not state['blink_detected']:
                state['blink_count'] += 1
                state['blink_detected'] = True
        else:
            state['blink_detected'] = False
        
        # Check for head movement
        has_movement, landmarks = face_detector.detect_head_movement(
            frame, state['previous_landmarks']
        )
        if has_movement:
            state['head_moved'] = True
        state['previous_landmarks'] = landmarks
        
        # Active check passed if both conditions met
        blink_ok = state['blink_count'] >= 1
        head_ok = state['head_moved']
        
        if blink_ok and head_ok:
            return True, "Active check passed"
        elif blink_ok:
            return False, "Please turn your head"
        elif head_ok:
            return False, "Please blink"
        else:
            return False, "Please blink and turn your head"
    
    def reset_active_check(self):
        """Reset active liveness check state"""
        self.active_check_state = {
            'blink_detected': False,
            'head_moved': False,
            'blink_count': 0,
            'previous_landmarks': None
        }
    
    def detect(self, face_roi, frame=None, face_detector=None, use_active_check=False):
        """
        Complete liveness detection pipeline
        Args:
            face_roi: Face region of interest
            frame: Full frame (for active check)
            face_detector: FaceDetector instance (for active check)
            use_active_check: Whether to perform active liveness check
        Returns: {
            'is_real': bool,
            'confidence': float,
            'active_check_passed': bool,
            'active_check_message': str
        }
        """
        result = {
            'is_real': False,
            'confidence': 0.0,
            'active_check_passed': False,
            'active_check_message': ''
        }
        
        # Passive check (always performed)
        is_real, confidence = self.passive_check(face_roi)
        result['is_real'] = is_real
        result['confidence'] = confidence
        
        # Active check (if enabled)
        if use_active_check and frame is not None and face_detector is not None:
            active_passed, active_message = self.active_check(frame, face_detector)
            result['active_check_passed'] = active_passed
            result['active_check_message'] = active_message
            
            # Both passive and active checks must pass
            result['is_real'] = is_real and active_passed
        
        return result
