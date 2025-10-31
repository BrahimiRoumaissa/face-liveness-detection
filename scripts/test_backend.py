"""
Quick backend test script
Tests if backend can start and imports work
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

def test_imports():
    """Test if all imports work"""
    print("Testing imports...")
    try:
        from utils.face_detector import FaceDetector
        print("  ✅ FaceDetector imported")
        
        from utils.liveness_detector import LivenessDetector
        print("  ✅ LivenessDetector imported")
        
        from utils.database import InferenceLogger
        print("  ✅ InferenceLogger imported")
        
        import cv2
        print("  ✅ OpenCV imported")
        
        import mediapipe as mp
        print("  ✅ MediaPipe imported")
        
        try:
            import tensorflow as tf
            print("  ✅ TensorFlow imported")
        except:
            print("  ⚠️  TensorFlow not available (model training will fail)")
        
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_components():
    """Test component initialization"""
    print("\nTesting component initialization...")
    try:
        from utils.face_detector import FaceDetector
        from utils.liveness_detector import LivenessDetector
        from utils.database import InferenceLogger
        
        face_detector = FaceDetector()
        print("  ✅ FaceDetector initialized")
        
        liveness_detector = LivenessDetector()
        print("  ✅ LivenessDetector initialized")
        
        logger = InferenceLogger()
        print("  ✅ InferenceLogger initialized")
        
        return True
    except Exception as e:
        print(f"  ❌ Initialization error: {e}")
        return False

def main():
    print("=" * 70)
    print("  Backend Component Test")
    print("=" * 70 + "\n")
    
    imports_ok = test_imports()
    components_ok = test_components() if imports_ok else False
    
    print("\n" + "=" * 70)
    if imports_ok and components_ok:
        print("  ✅ All backend components working!")
        print("\nYou can start the backend with:")
        print("  cd backend && python main.py")
    else:
        print("  ❌ Some components have issues")
        print("\nCheck error messages above and install missing dependencies:")
        print("  cd backend && pip install -r requirements.txt")
    print("=" * 70)

if __name__ == "__main__":
    main()

