"""
Dataset preprocessing utilities
Download and preprocess public datasets for training
"""
import os
import cv2
import numpy as np
from pathlib import Path
import shutil


def preprocess_image(image_path, output_size=(128, 128), normalize=True):
    """
    Preprocess a single image
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    # Resize
    img = cv2.resize(img, output_size)
    
    # Normalize if requested
    if normalize:
        img = img.astype(np.float32) / 255.0
    
    return img


def organize_dataset(source_dir, target_dir, real_folder="real", spoof_folder="spoof"):
    """
    Organize dataset into real/spoof folders
    """
    target_real = Path(target_dir) / real_folder
    target_spoof = Path(target_dir) / spoof_folder
    
    target_real.mkdir(parents=True, exist_ok=True)
    target_spoof.mkdir(parents=True, exist_ok=True)
    
    source_path = Path(source_dir)
    
    # Copy files based on folder structure or naming convention
    for img_path in source_path.rglob("*.jpg"):
        # Adjust this logic based on your dataset structure
        parent_name = img_path.parent.name.lower()
        
        if "real" in parent_name or "live" in parent_name or "genuine" in parent_name:
            shutil.copy(img_path, target_real / img_path.name)
        elif "spoof" in parent_name or "fake" in parent_name or "attack" in parent_name:
            shutil.copy(img_path, target_spoof / img_path.name)


def create_synthetic_dataset(output_dir="datasets/synthetic", num_samples=100):
    """
    Create a small synthetic dataset for testing (not for production)
    This is just for testing the pipeline when real dataset is not available
    """
    real_dir = Path(output_dir) / "real"
    spoof_dir = Path(output_dir) / "spoof"
    
    real_dir.mkdir(parents=True, exist_ok=True)
    spoof_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating synthetic dataset at {output_dir}")
    print("NOTE: This is for testing only. Use real datasets for production!")
    
    # Generate simple synthetic images (very basic)
    for i in range(num_samples):
        # "Real" face - more texture
        real_img = np.random.randint(50, 200, (128, 128, 3), dtype=np.uint8)
        # Add some structure
        real_img = cv2.GaussianBlur(real_img, (5, 5), 0)
        cv2.imwrite(str(real_dir / f"real_{i:04d}.jpg"), real_img)
        
        # "Spoof" - flatter, less texture
        spoof_img = np.random.randint(100, 150, (128, 128, 3), dtype=np.uint8)
        # More uniform (like printed photo)
        cv2.imwrite(str(spoof_dir / f"spoof_{i:04d}.jpg"), spoof_img)
    
    print(f"Created {num_samples} synthetic images in each class")


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "synthetic":
            create_synthetic_dataset()
        elif sys.argv[1] == "organize" and len(sys.argv) > 3:
            organize_dataset(sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  python preprocess_dataset.py synthetic  # Create synthetic test dataset")
        print("  python preprocess_dataset.py organize <source> <target>  # Organize dataset")

