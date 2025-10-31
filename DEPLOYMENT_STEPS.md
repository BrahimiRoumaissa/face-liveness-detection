# Step-by-Step Deployment Guide

This guide walks you through deploying the Face Liveness Detection System step by step.

## Prerequisites

- [ ] GitHub account
- [ ] Render/Railway account (for backend)
- [ ] Vercel account (for frontend)
- [ ] Code pushed to GitHub repository

---

## Step 1: Prepare Your Code

### 1.1 Initialize Git (if not done)

```bash
git init
git add .
git commit -m "Initial commit: Face Liveness Detection System"
```

### 1.2 Push to GitHub

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 1.3 Verify Structure

Make sure your project has:
- ✅ `backend/` directory with all files
- ✅ `frontend/` directory with all files
- ✅ `render.yaml` or `railway.json` (for backend)
- ✅ `vercel.json` (for frontend)

---

## Step 2: Deploy Backend (Choose One)

### Option A: Render.com

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Sign up or log in

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `face-liveness-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or set to `backend`)
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Copy your service URL (e.g., `https://face-liveness-backend.onrender.com`)

5. **Test Backend**
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should see: `{"status":"healthy","model_loaded":false}`

### Option B: Railway.app

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Sign up or log in

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Configure Service**
   - Railway auto-detects Python
   - In Settings → Deploy:
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Or add `railway.json` (already created)

4. **Deploy**
   - Railway automatically starts deploying
   - Wait for deployment to complete
   - Get your service URL from dashboard

5. **Test Backend**
   - Visit: `https://your-backend-url.railway.app/health`
   - Should see: `{"status":"healthy","model_loaded":false}`

---

## Step 3: Update CORS Settings

1. **Edit `backend/main.py`**

   Find this section:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Change this
       ...
   )
   ```

2. **Update with your frontend domain** (or keep "*" for now, update later):
   ```python
   allow_origins=[
       "https://your-frontend.vercel.app",
       "http://localhost:3000"  # For local testing
   ],
   ```

3. **Commit and push**:
   ```bash
   git add backend/main.py
   git commit -m "Update CORS settings"
   git push
   ```

4. **Wait for auto-deployment** (Render/Railway will redeploy)

---

## Step 4: Deploy Frontend (Vercel)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com
   - Sign up or log in (can use GitHub account)

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the repository

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `build` (or leave default)
   - **Install Command**: `npm install` (or leave default)

4. **Environment Variables**
   Click "Environment Variables" and add:
   
   - **REACT_APP_API_URL**
     - Value: `https://your-backend-url.onrender.com` (or Railway URL)
     - Example: `https://face-liveness-backend.onrender.com`
   
   - **REACT_APP_WS_URL**
     - Value: `wss://your-backend-url.onrender.com` (use `wss://` not `ws://`)
     - Example: `wss://face-liveness-backend.onrender.com`
     - ⚠️ **Important**: Replace `https://` with `wss://` for WebSocket

5. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for build
   - Copy your frontend URL (e.g., `https://face-liveness.vercel.app`)

---

## Step 5: Update Backend CORS (Again)

1. **Edit `backend/main.py`** with your actual frontend URL:
   ```python
   allow_origins=[
       "https://your-actual-frontend.vercel.app",
       "http://localhost:3000"
   ],
   ```

2. **Commit and push** (will auto-redeploy)

---

## Step 6: Test Everything

### 6.1 Test Backend
- Visit: `https://your-backend-url/health`
- Should return: `{"status":"healthy","model_loaded":false}`

### 6.2 Test Frontend
- Visit: `https://your-frontend-url`
- Should see the Face Liveness Detection interface

### 6.3 Test Full System
1. Click "Start Detection"
2. Allow camera permissions
3. Should see:
   - Camera feed
   - Face detection bounding box
   - Real/Spoof result

### 6.4 Test WebSocket
1. Open browser console (F12)
2. Look for WebSocket connection messages
3. Should see: "WebSocket connected"

---

## Step 7: Optional - Train and Upload Model

### 7.1 Train Model Locally
```bash
# Download dataset first, then:
python scripts/train_model.py
```

### 7.2 Upload Model to Backend

**For Render:**
- Model needs to be in your repo
- Commit `models/liveness_model.h5`
- Push to GitHub
- Backend will automatically have it

**For Railway:**
- Same as Render (commit and push)
- Or use Railway's file system (volatile)

**Note**: Model files are large. Consider:
- Using Git LFS
- Or uploading to cloud storage and downloading on startup

---

## Troubleshooting

### Backend Issues

**Problem**: Backend not starting
- Check logs in Render/Railway dashboard
- Verify `requirements.txt` has all dependencies
- Check Python version compatibility

**Problem**: 404 errors
- Verify start command includes `cd backend`
- Check root directory settings

**Problem**: WebSocket not working
- Verify using `wss://` in production
- Check CORS settings
- Ensure backend supports WebSockets

### Frontend Issues

**Problem**: API calls failing
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings on backend
- Test backend URL directly in browser

**Problem**: WebSocket connection fails
- Use `wss://` for HTTPS backends
- Check browser console for errors
- Verify backend WebSocket endpoint is accessible

**Problem**: Camera not working
- Requires HTTPS (production should be fine)
- Check browser permissions
- Test in incognito mode

---

## Environment Variables Summary

### Backend (Auto-set)
- `PORT` - Automatically set by hosting platform

### Frontend (Set in Vercel)
- `REACT_APP_API_URL` - Backend HTTP URL
- `REACT_APP_WS_URL` - Backend WebSocket URL (use `wss://`)

---

## Quick Reference

### Your URLs (Fill these in)

```
Backend URL:  https://__________________
Frontend URL: https://__________________

Backend Health Check: https://__________________/health
Frontend: https://__________________
```

### Useful Commands

```bash
# Test backend locally
cd backend
python main.py

# Test frontend locally
cd frontend
npm start

# Train model
python scripts/train_model.py

# Check deployment status
# - Check Render/Railway dashboard
# - Check Vercel dashboard
```

---

## Success Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] WebSocket connects successfully
- [ ] Camera access works
- [ ] Face detection works
- [ ] Liveness detection returns results

---

## Need Help?

- Check logs in your hosting platform dashboard
- Review `DEPLOYMENT.md` for detailed info
- Check `ARCHITECTURE.md` for system understanding
- Verify environment variables are set correctly

---

**Congratulations!** 🎉 Your Face Liveness Detection System should now be live!

