"""
Face Detection and Alignment using OpenCV and MediaPipe
"""
import cv2
import numpy as np
import mediapipe as mp


class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # Full range model for better accuracy
            min_detection_confidence=0.5
        )
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detect_face(self, frame):
        """
        Detect face in frame and return bounding box
        Returns: (x, y, width, height) or None if no face detected
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        if results.detections:
            detection = results.detections[0]  # Get first face
            bbox = detection.location_data.relative_bounding_box
            
            h, w, _ = frame.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)
            
            # Ensure coordinates are within frame bounds
            x = max(0, x)
            y = max(0, y)
            width = min(width, w - x)
            height = min(height, h - y)
            
            return (x, y, width, height)
        return None
    
    def extract_face_roi(self, frame, bbox=None):
        """
        Extract face region of interest from frame
        Args:
            frame: Input frame
            bbox: Optional bounding box (x, y, width, height)
        Returns: Resized face ROI (128x128) or None
        """
        if bbox is None:
            bbox = self.detect_face(frame)
        
        if bbox is None:
            return None
        
        x, y, w, h = bbox
        
        # Extract face with some padding
        padding = 20
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(frame.shape[1], x + w + padding)
        y_end = min(frame.shape[0], y + h + padding)
        
        face_roi = frame[y_start:y_end, x_start:x_end]
        
        if face_roi.size == 0:
            return None
        
        # Resize to 128x128 for model input
        face_roi = cv2.resize(face_roi, (128, 128))
        return face_roi
    
    def detect_blink(self, frame):
        """
        Detect blink using facial landmarks
        Returns: True if blink detected, False otherwise
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return False
        
        landmarks = results.multi_face_landmarks[0]
        
        # Left eye landmarks (MediaPipe indices)
        left_eye_top = landmarks.landmark[159].y
        left_eye_bottom = landmarks.landmark[145].y
        left_eye_left = landmarks.landmark[33].x
        left_eye_right = landmarks.landmark[133].x
        
        # Right eye landmarks
        right_eye_top = landmarks.landmark[386].y
        right_eye_bottom = landmarks.landmark[374].y
        right_eye_left = landmarks.landmark[362].x
        right_eye_right = landmarks.landmark[263].x
        
        # Calculate eye aspect ratios (EAR)
        left_ear = abs(left_eye_top - left_eye_bottom) / abs(left_eye_left - left_eye_right)
        right_ear = abs(right_eye_top - right_eye_bottom) / abs(right_eye_right - right_eye_left)
        
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Threshold for blink detection (lower EAR = more closed)
        blink_threshold = 0.25
        return avg_ear < blink_threshold
    
    def detect_head_movement(self, frame, prev_landmarks=None):
        """
        Detect head movement/turn
        Returns: (has_movement: bool, current_landmarks)
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return False, None
        
        landmarks = results.multi_face_landmarks[0]
        nose_tip = landmarks.landmark[4]  # Nose tip
        
        if prev_landmarks is None:
            return False, (nose_tip.x, nose_tip.y)
        
        # Calculate movement
        movement = np.sqrt(
            (nose_tip.x - prev_landmarks[0])**2 + 
            (nose_tip.y - prev_landmarks[1])**2
        )
        
        movement_threshold = 0.02
        return movement > movement_threshold, (nose_tip.x, nose_tip.y)
    
    def release(self):
        """Release resources"""
        self.face_detection.close()
        self.face_mesh.close()

