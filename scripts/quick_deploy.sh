#!/bin/bash
# Quick deployment script - prepares everything for deployment

echo "=================================="
echo "Quick Deployment Setup"
echo "=================================="

# Create necessary directories
mkdir -p models datasets scripts

# Check if git is initialized
if [ ! -d .git ]; then
    echo "⚠️  Git not initialized. Initializing..."
    git init
    echo "✅ Git initialized"
    echo "⚠️  Remember to:"
    echo "   1. git add ."
    echo "   2. git commit -m 'Initial commit'"
    echo "   3. Create GitHub repo and push"
fi

# Check Python dependencies
echo ""
echo "Checking Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

echo "Installing backend dependencies..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Backend dependencies ready"
cd ..

# Check Node dependencies
echo ""
echo "Checking Node dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install > /dev/null 2>&1
fi
echo "✅ Frontend dependencies ready"
cd ..

# Check model
echo ""
if [ ! -f "models/liveness_model.h5" ]; then
    echo "⚠️  Model not found. The system will use heuristic detection."
    echo "   Train a model with: python scripts/train_model.py"
else
    echo "✅ Model found"
fi

# Summary
echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Push code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for deployment'"
echo "   git remote add origin <your-repo-url>"
echo "   git push -u origin main"
echo ""
echo "2. Deploy backend (Render/Railway):"
echo "   - Follow instructions in DEPLOYMENT.md"
echo ""
echo "3. Deploy frontend (Vercel):"
echo "   - Follow instructions in DEPLOYMENT.md"
echo ""
echo "4. Run interactive guide:"
echo "   python scripts/deploy_guide.py"
echo ""

