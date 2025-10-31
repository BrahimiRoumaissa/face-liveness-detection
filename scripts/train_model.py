"""
Automated Model Training Script
Trains the face liveness detection model
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from model.train_model import train_model


def main():
    """Main training function"""
    print("=" * 60)
    print("Face Liveness Detection Model Training")
    print("=" * 60)
    
    # Check if dataset exists
    dataset_dir = Path("datasets")
    real_dir = dataset_dir / "real"
    spoof_dir = dataset_dir / "spoof"
    
    if not real_dir.exists() or not spoof_dir.exists():
        print("\n❌ Dataset not found!")
        print(f"Expected structure:")
        print(f"  {real_dir}/")
        print(f"  {spoof_dir}/")
        print("\nPlease:")
        print("1. Download a dataset (CelebA-Spoof, CASIA-FASD, or Replay-Attack)")
        print("2. Organize images into datasets/real/ and datasets/spoof/")
        print("3. Run: python scripts/download_dataset.py --help")
        return
    
    # Count images
    real_count = len(list(real_dir.glob("*.jpg")))
    spoof_count = len(list(spoof_dir.glob("*.jpg")))
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  Real images: {real_count}")
    print(f"  Spoof images: {spoof_count}")
    print(f"  Total: {real_count + spoof_count}")
    
    if real_count == 0 or spoof_count == 0:
        print("\n❌ Insufficient data for training!")
        print("Need both real and spoof images.")
        return
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Training parameters
    epochs = 10
    batch_size = 32
    
    print(f"\n🚀 Starting training...")
    print(f"  Epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Model will be saved to: models/liveness_model.h5")
    print("\n" + "=" * 60)
    
    try:
        # Train model
        model, history = train_model(
            data_dir=str(dataset_dir),
            model_save_path=str(models_dir / "liveness_model.h5"),
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            test_split=0.1
        )
        
        print("\n" + "=" * 60)
        print("✅ Training completed successfully!")
        print(f"✅ Model saved to: models/liveness_model.h5")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()

