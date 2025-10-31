#!/bin/bash
# Start script for backend server

# Check if model exists
if [ ! -f "../models/liveness_model.h5" ]; then
    echo "Warning: Model file not found at models/liveness_model.h5"
    echo "The system will use heuristic-based detection until a model is trained."
    echo "To train a model, run: python model/train_model.py"
fi

# Start server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

