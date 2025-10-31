# Deployment Guide

## Backend Deployment (Render/Railway)

### Render.com

1. **Create New Web Service**
   - Connect your GitHub repository
   - Select "Python" as the environment
   - Build command: `cd backend && pip install -r requirements.txt`
   - Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables** (if needed):
   - `PORT`: Auto-set by Render
   - Add any other custom variables

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your service URL (e.g., `https://your-app.onrender.com`)

### Railway.app

1. **Create New Project**
   - Connect your GitHub repository
   - Railway auto-detects Python

2. **Configure**:
   - Create `Procfile` in root:
     ```
     web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - Or add start command in Railway dashboard:
     ```
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Environment Variables**:
   - Railway auto-sets `PORT`
   - Add any other needed variables

4. **Deploy**:
   - Push to main branch triggers deployment
   - Get your service URL from Railway dashboard

## Frontend Deployment (Vercel)

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Set build command: npm run build
# - Set output directory: build
```

### Option 2: Vercel Dashboard

1. **Import Project**
   - Go to vercel.com
   - Click "New Project"
   - Import your GitHub repository

2. **Configure**:
   - Framework Preset: Create React App
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

3. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   REACT_APP_WS_URL=wss://your-backend.railway.app
   ```
   **Note**: Use `wss://` (secure WebSocket) for HTTPS backends

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live!

## WebSocket Configuration

### Important Notes:

1. **Secure WebSocket (WSS)**:
   - In production with HTTPS, use `wss://` instead of `ws://`
   - Update `REACT_APP_WS_URL` in Vercel environment variables

2. **CORS Settings**:
   - Update `allow_origins` in `backend/main.py`:
     ```python
     allow_origins=["https://your-frontend.vercel.app"]
     ```

3. **WebSocket Support**:
   - Render: Supports WebSockets
   - Railway: Supports WebSockets
   - Both platforms handle WebSocket upgrades automatically

## Post-Deployment Checklist

- [ ] Backend is accessible at HTTPS URL
- [ ] Frontend environment variables point to backend
- [ ] WebSocket URL uses `wss://` protocol
- [ ] CORS settings allow frontend domain
- [ ] Model file (`liveness_model.h5`) is accessible (or use heuristic mode)
- [ ] Database file permissions allow writes (for SQLite)

## Troubleshooting Deployment

### Backend Issues

**Problem**: Backend crashes on startup
- Check logs for import errors
- Ensure all dependencies in `requirements.txt`
- Verify Python version (3.8+)

**Problem**: WebSocket not connecting
- Verify backend supports WebSockets
- Check CORS settings
- Ensure using `wss://` with HTTPS

**Problem**: Model not loading
- Verify model file path
- Check file permissions
- System works without model (uses heuristics)

### Frontend Issues

**Problem**: API calls failing
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings on backend
- Test backend URL directly

**Problem**: WebSocket connection fails
- Use `wss://` for HTTPS backends
- Check browser console for errors
- Verify backend WebSocket endpoint is accessible

**Problem**: Camera not working
- Requires HTTPS in production
- Check browser permissions
- Verify camera access in browser settings

## Environment Variables Summary

### Backend
- `PORT`: Server port (auto-set by platform)

### Frontend
- `REACT_APP_API_URL`: Backend HTTP URL
- `REACT_APP_WS_URL`: Backend WebSocket URL (use `wss://`)

## Example Deployment URLs

After deployment, you should have:
- Backend: `https://face-liveness-backend.railway.app`
- Frontend: `https://face-liveness.vercel.app`

Update frontend `.env` or Vercel environment variables:
```
REACT_APP_API_URL=https://face-liveness-backend.railway.app
REACT_APP_WS_URL=wss://face-liveness-backend.railway.app
```

