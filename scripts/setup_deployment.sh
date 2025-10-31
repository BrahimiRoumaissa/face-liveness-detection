#!/bin/bash
# Setup script for deployment preparation

echo "=================================="
echo "Deployment Setup Script"
echo "=================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Face Liveness Detection System"
    echo "✅ Git repository initialized"
fi

# Create .env.example files
echo ""
echo "Creating environment variable templates..."

# Backend .env.example
cat > backend/.env.example << EOF
# Backend Environment Variables
PORT=8000
# Add other backend variables here
EOF

# Frontend .env.example
cat > frontend/.env.example << EOF
# Frontend Environment Variables
# Update these with your production URLs after deployment
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
EOF

echo "✅ Environment variable templates created"

# Check if models directory exists
if [ ! -f "models/liveness_model.h5" ]; then
    echo ""
    echo "⚠️  Warning: Model file not found (models/liveness_model.h5)"
    echo "   The system will work with heuristic detection."
    echo "   Train a model using: python scripts/train_model.py"
fi

# Create deployment checklist
cat > DEPLOYMENT_CHECKLIST.md << EOF
# Deployment Checklist

## Pre-Deployment

- [ ] Model trained and saved to models/liveness_model.h5
- [ ] All dependencies installed and tested locally
- [ ] Git repository initialized and code committed
- [ ] Environment variables documented

## Backend Deployment (Render/Railway)

- [ ] Create account on Render/Railway
- [ ] Connect GitHub repository
- [ ] Configure build settings:
  - Build command: \`cd backend && pip install -r requirements.txt\`
  - Start command: \`cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT\`
- [ ] Deploy and get backend URL
- [ ] Test backend health endpoint

## Frontend Deployment (Vercel)

- [ ] Create account on Vercel
- [ ] Connect GitHub repository
- [ ] Configure settings:
  - Root Directory: \`frontend\`
  - Build Command: \`npm run build\`
  - Output Directory: \`build\`
- [ ] Set environment variables:
  - REACT_APP_API_URL (backend HTTP URL)
  - REACT_APP_WS_URL (backend WebSocket URL with wss://)
- [ ] Deploy and get frontend URL

## Post-Deployment

- [ ] Update CORS in backend/main.py with frontend URL
- [ ] Test full system end-to-end
- [ ] Verify WebSocket connection works
- [ ] Test camera access in production

## URLs to Save

Backend URL: _______________________
Frontend URL: _______________________
EOF

echo ""
echo "✅ Deployment checklist created: DEPLOYMENT_CHECKLIST.md"
echo ""
echo "Next steps:"
echo "1. Review DEPLOYMENT_CHECKLIST.md"
echo "2. Push code to GitHub"
echo "3. Follow deployment instructions in DEPLOYMENT.md"
echo ""
echo "=================================="

