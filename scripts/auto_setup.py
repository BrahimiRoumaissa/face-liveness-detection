"""
Automated Setup Script - Non-interactive version
Checks status and provides instructions
"""
import os
from pathlib import Path


def check_status():
    """Check current project status"""
    status = {
        'git': Path('.git').exists(),
        'dataset': Path('datasets/real').exists() and Path('datasets/spoof').exists(),
        'model': Path('models/liveness_model.h5').exists(),
        'backend_deps': Path('backend/requirements.txt').exists(),
        'frontend_deps': Path('frontend/package.json').exists(),
        'deployment_configs': {
            'render': Path('render.yaml').exists(),
            'railway': Path('railway.json').exists(),
            'vercel': Path('vercel.json').exists()
        }
    }
    
    # Count dataset images
    if status['dataset']:
        real_count = len(list(Path('datasets/real').glob('*.jpg')))
        spoof_count = len(list(Path('datasets/spoof').glob('*.jpg')))
        status['dataset_count'] = {'real': real_count, 'spoof': spoof_count}
    
    return status


def print_status():
    """Print current status"""
    print("\n" + "=" * 70)
    print("  Project Status Check")
    print("=" * 70 + "\n")
    
    status = check_status()
    
    # Git
    print(f"{'✅' if status['git'] else '❌'} Git repository")
    
    # Dataset
    if status['dataset']:
        counts = status['dataset_count']
        print(f"✅ Dataset ({counts['real']} real, {counts['spoof']} spoof images)")
    else:
        print("❌ Dataset not found")
    
    # Model
    print(f"{'✅' if status['model'] else '❌'} Trained model")
    
    # Dependencies
    print(f"{'✅' if status['backend_deps'] else '❌'} Backend dependencies")
    print(f"{'✅' if status['frontend_deps'] else '❌'} Frontend dependencies")
    
    # Deployment configs
    print(f"\nDeployment configs:")
    print(f"  {'✅' if status['deployment_configs']['render'] else '❌'} render.yaml")
    print(f"  {'✅' if status['deployment_configs']['railway'] else '❌'} railway.json")
    print(f"  {'✅' if status['deployment_configs']['vercel'] else '❌'} vercel.json")
    
    return status


def print_next_steps(status):
    """Print next steps based on status"""
    print("\n" + "=" * 70)
    print("  Next Steps")
    print("=" * 70 + "\n")
    
    steps = []
    
    if not status['git']:
        steps.append("1. Initialize git: git init && git add . && git commit -m 'Initial commit'")
    
    if not status['dataset']:
        steps.append("2. Download dataset:")
        steps.append("   - CASIA-FASD: http://www.cbsr.ia.ac.cn/english/CASIA-FASD.asp")
        steps.append("   - Or run: python backend/model/preprocess_dataset.py synthetic")
        steps.append("   - Then: python scripts/download_dataset.py --help")
    
    if status['dataset'] and not status['model']:
        counts = status['dataset_count']
        if counts['real'] > 0 and counts['spoof'] > 0:
            steps.append("3. Train model: python scripts/train_model.py")
        else:
            steps.append("3. Organize dataset (need images in datasets/real/ and datasets/spoof/)")
    
    if status['git']:
        steps.append("4. Push to GitHub: git push origin main")
        steps.append("5. Deploy backend (Render/Railway) - see DEPLOYMENT_STEPS.md")
        steps.append("6. Deploy frontend (Vercel) - see DEPLOYMENT_STEPS.md")
        steps.append("7. Update environment variables in Vercel")
    
    if not steps:
        print("✅ Everything is ready! You can deploy now.")
        print("\nFollow: DEPLOYMENT_STEPS.md for deployment instructions")
    else:
        for step in steps:
            print(step)


def main():
    """Main function"""
    print_status()
    status = check_status()
    print_next_steps(status)
    
    print("\n" + "=" * 70)
    print("  Quick Commands")
    print("=" * 70 + "\n")
    print("Check status:        python scripts/auto_setup.py")
    print("Setup dataset:       python scripts/download_dataset.py --help")
    print("Train model:         python scripts/train_model.py")
    print("Full setup:          python scripts/setup_complete.py")
    print("Deployment guide:    python scripts/deploy_guide.py")
    print("\nSee QUICK_START.md for detailed instructions")


if __name__ == "__main__":
    main()

