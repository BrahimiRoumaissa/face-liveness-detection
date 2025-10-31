# 🚀 DEPLOY NOW - Step-by-Step Guide

## ✅ Current Status

**Everything is ready!**
- ✅ Model trained (100% accuracy!)
- ✅ All code committed
- ✅ Deployment configs ready
- ✅ Documentation complete

## Quick Deployment (45 minutes total)

### 📤 Step 1: Push to GitHub (5 minutes)

#### 1.1 Create GitHub Repository

1. Go to: https://github.com/new
2. **Repository name**: `face-liveness-detection` (or your choice)
3. **Description**: "Face Liveness Detection System - Real-time spoof detection"
4. **Visibility**: Public or Private (your choice)
5. **⚠️ IMPORTANT**: **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

#### 1.2 Push Your Code

Copy the commands from GitHub (or use these):

```bash
# Add remote (replace YOUR_USERNAME and YOUR_REPO with your actual values)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin master
```

**Or use the helper script:**
```bash
python scripts/prepare_github.py
```

---

### 🌐 Step 2: Deploy Backend (15 minutes)

Choose **ONE** platform:

#### Option A: Render.com (Recommended)

1. **Sign up**: https://render.com
   - Use GitHub to sign in (easiest)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Click "Connect account" → Connect GitHub
   - Select your repository: `face-liveness-detection`

3. **Configure** (Render auto-detects `render.yaml` ✅):
   - **Name**: `face-liveness-backend`
   - **Region**: Choose closest to you
   - **Branch**: `master`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build
   - Watch the logs as it builds

5. **Get Your URL**:
   - Once deployed, copy your service URL
   - Format: `https://face-liveness-backend-xxxx.onrender.com`
   - **SAVE THIS URL!** You'll need it for frontend

6. **Test Backend**:
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should see: `{"status":"healthy","model_loaded":true}` ✅

#### Option B: Railway.app

1. **Sign up**: https://railway.app
   - Use GitHub to sign in

2. **New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**:
   - Railway auto-detects Python ✅
   - In Settings → Deploy:
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Or Railway will use `railway.json` automatically

4. **Deploy**:
   - Railway starts building automatically
   - Wait 3-5 minutes

5. **Get Your URL**:
   - From dashboard, copy your service URL
   - Format: `https://your-app.up.railway.app`
   - **SAVE THIS URL!**

6. **Test Backend**:
   - Visit: `https://your-backend-url/health`
   - Should see: `{"status":"healthy","model_loaded":true}` ✅

---

### 🎨 Step 3: Deploy Frontend (15 minutes)

#### Using Vercel

1. **Sign up**: https://vercel.com
   - Click "Sign up" → Use GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import from GitHub
   - Select your repository: `face-liveness-detection`

3. **Configure Project**:
   - **Framework Preset**: **Create React App**
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT**
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `build` (or leave default)
   - **Install Command**: `npm install` (or leave default)

4. **Environment Variables** (CRITICAL!):
   - Click "Environment Variables" section
   - Add these **TWO** variables:

   **Variable 1:**
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (your actual backend URL)
   - **Environment**: Production, Preview, Development (check all)

   **Variable 2:**
   - **Key**: `REACT_APP_WS_URL`
   - **Value**: `wss://your-backend-url.onrender.com` ⚠️ **Use `wss://` not `ws://`**
   - **Environment**: Production, Preview, Development (check all)

   **Example:**
   ```
   REACT_APP_API_URL = https://face-liveness-backend-abc123.onrender.com
   REACT_APP_WS_URL = wss://face-liveness-backend-abc123.onrender.com
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-5 minutes for build
   - Watch build logs

6. **Get Your URL**:
   - Once deployed, copy your frontend URL
   - Format: `https://face-liveness-detection.vercel.app`
   - **SAVE THIS URL!**

---

### ⚙️ Step 4: Update CORS (5 minutes)

1. **Edit `backend/main.py`**:
   - Find the CORS middleware section (around line 20)
   - Update `allow_origins`:

   ```python
   allow_origins=[
       "https://your-actual-frontend.vercel.app",  # Your real frontend URL
       "http://localhost:3000"  # Keep for local testing
   ],
   ```

2. **Commit and Push**:
   ```bash
   git add backend/main.py
   git commit -m "Update CORS for production"
   git push
   ```

3. **Auto-Redeploy**:
   - Render/Railway will automatically detect the push
   - It will rebuild and redeploy (2-3 minutes)
   - No action needed!

---

### ✅ Step 5: Test Everything (5 minutes)

#### Test 1: Backend Health
- Visit: `https://your-backend-url/health`
- Should see: `{"status":"healthy","model_loaded":true}`

#### Test 2: Frontend Loads
- Visit: `https://your-frontend-url`
- Should see the Face Liveness Detection interface

#### Test 3: Full System
1. Click **"Start Detection"**
2. **Allow camera permissions** when prompted
3. Point camera at your face
4. Should see:
   - ✅ Camera feed
   - ✅ Face detection bounding box (green/red)
   - ✅ "REAL" or "SPOOF" result
   - ✅ Confidence percentage

#### Test 4: WebSocket
1. Open browser console (F12)
2. Look for: `"WebSocket connected"`
3. Should see frame processing messages

---

## 📋 Deployment Checklist

Use this to track your progress:

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Backend deployed (Render/Railway)
- [ ] Backend URL saved
- [ ] Backend health check passes
- [ ] Frontend deployed (Vercel)
- [ ] Environment variables set in Vercel
- [ ] Frontend URL saved
- [ ] CORS updated in backend/main.py
- [ ] CORS changes committed and pushed
- [ ] Backend auto-redeployed
- [ ] Frontend loads correctly
- [ ] Camera access works
- [ ] Face detection works
- [ ] WebSocket connection works
- [ ] Full system test passes

---

## 🎉 Success!

Once all checkboxes are checked:

**Your Face Liveness Detection System is LIVE!** 🚀

### Your URLs (Fill these in):

```
Backend URL:  https://________________________
Frontend URL: https://________________________
```

---

## 🔧 Troubleshooting

### Backend Won't Start
- Check logs in Render/Railway dashboard
- Verify `requirements.txt` has all dependencies
- Check Python version (should be 3.8+)

### Frontend Can't Connect to Backend
- Verify `REACT_APP_API_URL` is correct
- Check CORS settings in backend
- Ensure backend URL is accessible (test in browser)

### WebSocket Connection Fails
- **MOST COMMON**: Not using `wss://` - must use `wss://` not `ws://`
- Check `REACT_APP_WS_URL` in Vercel environment variables
- Verify backend supports WebSockets (should work automatically)

### Camera Not Working
- Requires HTTPS (production should be fine)
- Check browser permissions
- Try different browser
- Check browser console for errors

---

## 📞 Quick Help

**Check status**: `python scripts/auto_setup.py`

**View logs**:
- Render: Dashboard → Your Service → Logs
- Railway: Dashboard → Your Service → Logs
- Vercel: Dashboard → Your Project → Deployments → View Logs

**Redeploy**:
- Push to GitHub (auto-redeploys)
- Or manually trigger in dashboard

---

**Ready? Start with Step 1 above!** 🚀

Good luck! Everything is ready to go live! 🎉

