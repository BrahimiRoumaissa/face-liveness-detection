#!/bin/bash
# Complete automated setup script

echo "=================================="
echo "Complete Automated Setup"
echo "=================================="

# Step 1: Check Python
echo ""
echo "Step 1: Checking Python..."
python --version || { echo "❌ Python not found"; exit 1; }
echo "✅ Python OK"

# Step 2: Check Node
echo ""
echo "Step 2: Checking Node..."
node --version || echo "⚠️  Node not found (frontend needs it)"
npm --version || echo "⚠️  npm not found (frontend needs it)"

# Step 3: Install backend deps
echo ""
echo "Step 3: Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate || source venv/Scripts/activate
pip install -q -r requirements.txt
echo "✅ Backend dependencies installed"
cd ..

# Step 4: Install frontend deps
echo ""
echo "Step 4: Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install --silent
fi
echo "✅ Frontend dependencies installed"
cd ..

# Step 5: Check dataset
echo ""
echo "Step 5: Checking dataset..."
if [ -d "datasets/real" ] && [ -d "datasets/spoof" ]; then
    real_count=$(find datasets/real -name "*.jpg" | wc -l)
    spoof_count=$(find datasets/spoof -name "*.jpg" | wc -l)
    echo "✅ Dataset found: $real_count real, $spoof_count spoof"
else
    echo "⚠️  Dataset not found"
fi

# Step 6: Check model
echo ""
echo "Step 6: Checking model..."
if [ -f "models/liveness_model.h5" ]; then
    echo "✅ Model found"
else
    echo "⚠️  Model not found (system will use heuristics)"
fi

# Step 7: Check git
echo ""
echo "Step 7: Checking git..."
if [ -d ".git" ]; then
    echo "✅ Git repository initialized"
    git status --short | head -5
else
    echo "⚠️  Git not initialized"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Train model (optional): python scripts/train_model.py"
echo "2. Push to GitHub: git push origin main"
echo "3. Deploy: See DEPLOYMENT_STEPS.md"

