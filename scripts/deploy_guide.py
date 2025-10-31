"""
Interactive Deployment Guide
Helps you deploy the Face Liveness Detection System
"""
import os
from pathlib import Path


def print_section(title):
    """Print a formatted section title"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def check_prerequisites():
    """Check if prerequisites are met"""
    print_section("Prerequisites Check")
    
    checks = {
        "Git installed": os.system("git --version") == 0,
        "Git repository initialized": Path(".git").exists(),
        "Backend dependencies": Path("backend/requirements.txt").exists(),
        "Frontend package.json": Path("frontend/package.json").exists(),
    }
    
    all_ok = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_ok = False
    
    return all_ok


def backend_deployment_guide():
    """Backend deployment instructions"""
    print_section("Backend Deployment (Render or Railway)")
    
    print("Choose your platform:")
    print("1. Render.com")
    print("2. Railway.app")
    print("3. Both (instructions for both)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        print("\n" + "-" * 70)
        print("RENDER.COM DEPLOYMENT")
        print("-" * 70)
        print("\nSteps:")
        print("1. Go to https://render.com and sign up/login")
        print("2. Click 'New +' → 'Web Service'")
        print("3. Connect your GitHub repository")
        print("4. Configure settings:")
        print("   - Name: face-liveness-backend")
        print("   - Environment: Python 3")
        print("   - Build Command: cd backend && pip install -r requirements.txt")
        print("   - Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT")
        print("5. Click 'Create Web Service'")
        print("6. Wait for deployment (5-10 minutes)")
        print("7. Copy your service URL (e.g., https://your-app.onrender.com)")
        print("\nOr use render.yaml:")
        print("   render.yaml file is ready - Render can auto-detect it!")
    
    if choice in ['2', '3']:
        print("\n" + "-" * 70)
        print("RAILWAY.APP DEPLOYMENT")
        print("-" * 70)
        print("\nSteps:")
        print("1. Go to https://railway.app and sign up/login")
        print("2. Click 'New Project' → 'Deploy from GitHub repo'")
        print("3. Select your repository")
        print("4. Railway will auto-detect Python and start building")
        print("5. Configure in Settings:")
        print("   - Add start command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT")
        print("6. Deploy")
        print("7. Get your service URL from the dashboard")
        print("\nOr use railway.json:")
        print("   railway.json file is ready - Railway can auto-detect it!")
    
    backend_url = input("\n📝 Enter your backend URL (or press Enter to skip): ").strip()
    return backend_url


def frontend_deployment_guide(backend_url=""):
    """Frontend deployment instructions"""
    print_section("Frontend Deployment (Vercel)")
    
    print("Steps:")
    print("1. Go to https://vercel.com and sign up/login")
    print("2. Click 'New Project'")
    print("3. Import your GitHub repository")
    print("4. Configure project settings:")
    print("   - Framework Preset: Create React App")
    print("   - Root Directory: frontend")
    print("   - Build Command: npm run build")
    print("   - Output Directory: build")
    print("5. Add Environment Variables:")
    
    if backend_url:
        ws_url = backend_url.replace("https://", "wss://").replace("http://", "ws://")
        print(f"   - REACT_APP_API_URL: {backend_url}")
        print(f"   - REACT_APP_WS_URL: {ws_url}")
    else:
        print("   - REACT_APP_API_URL: (your backend URL)")
        print("   - REACT_APP_WS_URL: (your backend WebSocket URL with wss://)")
    
    print("6. Click 'Deploy'")
    print("7. Wait for build and get your frontend URL")
    
    frontend_url = input("\n📝 Enter your frontend URL (or press Enter to skip): ").strip()
    return frontend_url


def create_env_template(backend_url, frontend_url):
    """Create environment variable template"""
    if not backend_url or not frontend_url:
        print("\n⚠️  Skipping .env file creation (URLs not provided)")
        return
    
    ws_url = backend_url.replace("https://", "wss://").replace("http://", "ws://")
    
    env_content = f"""# Production Environment Variables
# Backend
BACKEND_URL={backend_url}

# Frontend
REACT_APP_API_URL={backend_url}
REACT_APP_WS_URL={ws_url}
FRONTEND_URL={frontend_url}
"""
    
    env_file = Path(".env.production")
    env_file.write_text(env_content)
    print(f"\n✅ Created {env_file} with your URLs")
    
    # Also update vercel example
    vercel_env_example = Path("frontend/.env.production.example")
    vercel_env_content = f"""REACT_APP_API_URL={backend_url}
REACT_APP_WS_URL={ws_url}
"""
    vercel_env_example.write_text(vercel_env_content)
    print(f"✅ Created {vercel_env_example}")


def update_cors_instructions(backend_url):
    """Instructions for updating CORS"""
    if not backend_url:
        return
    
    frontend_domain = input("\n📝 Enter your frontend domain (e.g., your-app.vercel.app): ").strip()
    
    if frontend_domain:
        print_section("CORS Configuration")
        print("Update backend/main.py CORS settings:")
        print(f"\nReplace:")
        print('    allow_origins=["*"],')
        print("\nWith:")
        print(f'    allow_origins=["https://{frontend_domain}", "http://localhost:3000"],')
        print("\nThis allows your frontend to access the backend.")


def main():
    """Main deployment guide"""
    print_section("Face Liveness Detection - Deployment Guide")
    
    print("This script will guide you through deploying your application.")
    print("Make sure you have:")
    print("  - Git repository initialized and pushed to GitHub")
    print("  - Backend and frontend code ready")
    print("  - Accounts on Render/Railway and Vercel")
    
    input("\nPress Enter to continue...")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Some prerequisites are missing. Please fix them and run again.")
        return
    
    print("\n✅ All prerequisites met!")
    
    # Backend deployment
    backend_url = backend_deployment_guide()
    
    # Frontend deployment
    frontend_url = frontend_deployment_guide(backend_url)
    
    # Create env templates
    if backend_url and frontend_url:
        create_env_template(backend_url, frontend_url)
    
    # CORS instructions
    if backend_url:
        update_cors_instructions(backend_url)
    
    # Final steps
    print_section("Final Steps")
    print("After deployment:")
    print("1. Test your backend:")
    print(f"   {backend_url}/health")
    print("2. Test your frontend:")
    print(f"   {frontend_url}")
    print("3. Test WebSocket connection in browser console")
    print("4. Allow camera permissions and test detection")
    
    print("\n✅ Deployment guide complete!")
    print("\nIf you encounter issues, check:")
    print("  - DEPLOYMENT.md for detailed instructions")
    print("  - Backend/frontend logs in your hosting platform")
    print("  - Browser console for frontend errors")


if __name__ == "__main__":
    main()

