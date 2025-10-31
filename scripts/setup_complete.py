"""
Complete Setup Script - Handles dataset, training, and deployment prep
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_git_repo():
    """Check if git is initialized"""
    if not Path(".git").exists():
        print_header("Git Repository Setup")
        print("Git repository not found. Initializing...")
        subprocess.run(["git", "init"], check=True)
        print("✅ Git initialized")
        
        print("\nNext steps:")
        print("1. Create a repository on GitHub")
        print("2. Run: git remote add origin <your-repo-url>")
        print("3. Run: git add .")
        print("4. Run: git commit -m 'Initial commit'")
        print("5. Run: git push -u origin main")
        return False
    return True


def dataset_setup():
    """Help set up dataset"""
    print_header("Dataset Setup")
    
    dataset_dir = Path("datasets")
    real_dir = dataset_dir / "real"
    spoof_dir = dataset_dir / "spoof"
    
    if real_dir.exists() and spoof_dir.exists():
        real_count = len(list(real_dir.glob("*.jpg")))
        spoof_count = len(list(spoof_dir.glob("*.jpg")))
        
        if real_count > 0 and spoof_count > 0:
            print(f"✅ Dataset found!")
            print(f"   Real images: {real_count}")
            print(f"   Spoof images: {spoof_count}")
            return True
    
    print("📦 Dataset not found. Here's how to get one:")
    print("\nOption 1: CASIA-FASD (Free, requires registration)")
    print("  1. Visit: http://www.cbsr.ia.ac.cn/english/CASIA-FASD.asp")
    print("  2. Register and download")
    print("  3. Extract and run:")
    print("     python scripts/download_dataset.py --dataset casia --source-dir <extracted_path>")
    
    print("\nOption 2: Replay-Attack (Free, requires registration)")
    print("  1. Visit: https://www.idiap.ch/en/dataset/replayattack")
    print("  2. Register and download")
    print("  3. Extract and run:")
    print("     python scripts/download_dataset.py --dataset replay --source-dir <extracted_path>")
    
    print("\nOption 3: CelebA-Spoof (Large dataset)")
    print("  1. Visit: https://mmlab.ie.cuhk.edu.hk/projects/CelebA_Spoof.html")
    print("  2. Requires approval, download instructions provided")
    
    print("\nOption 4: Create synthetic test dataset (for testing only)")
    print("  Run: python backend/model/preprocess_dataset.py synthetic")
    
    return False


def train_model_if_ready():
    """Train model if dataset is ready"""
    print_header("Model Training")
    
    dataset_dir = Path("datasets")
    real_dir = dataset_dir / "real"
    spoof_dir = dataset_dir / "spoof"
    
    if not real_dir.exists() or not spoof_dir.exists():
        print("⚠️  Dataset not ready. Skipping training.")
        return False
    
    real_count = len(list(real_dir.glob("*.jpg")))
    spoof_count = len(list(spoof_dir.glob("*.jpg")))
    
    if real_count == 0 or spoof_count == 0:
        print("⚠️  Insufficient data. Need both real and spoof images.")
        return False
    
    model_path = Path("models/liveness_model.h5")
    if model_path.exists():
        response = input(f"\nModel already exists at {model_path}. Retrain? (y/N): ").strip().lower()
        if response != 'y':
            print("✅ Using existing model")
            return True
    
    print(f"📊 Dataset ready: {real_count} real, {spoof_count} spoof images")
    response = input("\nStart training? This may take 30-60 minutes. (y/N): ").strip().lower()
    
    if response == 'y':
        print("\n🚀 Starting training...")
        try:
            # Import and run training
            sys.path.insert(0, str(Path("backend")))
            from model.train_model import train_model
            
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            model, history = train_model(
                data_dir=str(dataset_dir),
                model_save_path=str(models_dir / "liveness_model.h5"),
                epochs=10,
                batch_size=32
            )
            
            print("\n✅ Training completed!")
            return True
        except Exception as e:
            print(f"\n❌ Training failed: {e}")
            print("You can train manually later with: python scripts/train_model.py")
            return False
    else:
        print("⏭️  Skipping training. Train later with: python scripts/train_model.py")
        return False


def deployment_prep():
    """Prepare for deployment"""
    print_header("Deployment Preparation")
    
    # Check config files
    configs_ok = True
    if not Path("render.yaml").exists():
        print("⚠️  render.yaml not found (optional for Render)")
        configs_ok = False
    
    if not Path("railway.json").exists():
        print("⚠️  railway.json not found (optional for Railway)")
        configs_ok = False
    
    if not Path("vercel.json").exists():
        print("⚠️  vercel.json not found")
        configs_ok = False
    else:
        print("✅ vercel.json found")
    
    if configs_ok:
        print("\n✅ Deployment config files ready!")
    
    # Check git
    if check_git_repo():
        print("✅ Git repository ready")
        print("\nNext steps for deployment:")
        print("1. Push code to GitHub")
        print("2. Follow DEPLOYMENT_STEPS.md for detailed instructions")
        print("3. Or run: python scripts/deploy_guide.py")
    else:
        print("\n⚠️  Initialize git repository first")
    
    return True


def main():
    """Main setup flow"""
    print_header("Face Liveness Detection - Complete Setup")
    
    print("This script will help you:")
    print("1. Set up dataset")
    print("2. Train model")
    print("3. Prepare for deployment")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Dataset
    dataset_ready = dataset_setup()
    
    # Step 2: Training
    if dataset_ready:
        train_model_if_ready()
    else:
        print("\n⏭️  Skipping training (no dataset)")
        print("   Train later with: python scripts/train_model.py")
    
    # Step 3: Deployment prep
    deployment_prep()
    
    # Summary
    print_header("Setup Summary")
    print("✅ Setup complete!")
    print("\nWhat you have:")
    print("  ✅ Project structure")
    print("  ✅ Backend (FastAPI)")
    print("  ✅ Frontend (React)")
    print("  ✅ Training scripts")
    print("  ✅ Deployment configs")
    
    print("\nNext steps:")
    if not dataset_ready:
        print("  1. Download a dataset (see instructions above)")
        print("  2. Organize it into datasets/real/ and datasets/spoof/")
        print("  3. Train model: python scripts/train_model.py")
    
    print("\n  Deployment:")
    print("  1. Push code to GitHub")
    print("  2. Follow: DEPLOYMENT_STEPS.md")
    print("  3. Or run: python scripts/deploy_guide.py")
    
    print("\n  Local testing:")
    print("  1. Backend: cd backend && python main.py")
    print("  2. Frontend: cd frontend && npm start")


if __name__ == "__main__":
    main()

