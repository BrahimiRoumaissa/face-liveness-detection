# Quick Start Guide - Complete Setup

This guide walks you through all the steps you requested:
1. Download a dataset
2. Train the model
3. Deploy backend to Render/Railway
4. Deploy frontend to Vercel
5. Update environment variables

---

## 📦 Step 1: Download Dataset

### Option A: CASIA-FASD (Recommended for beginners)

1. **Visit**: http://www.cbsr.ia.ac.cn/english/CASIA-FASD.asp
2. **Register** and download the dataset
3. **Extract** the downloaded file
4. **Organize** using our script:
   ```bash
   python scripts/download_dataset.py --dataset casia --source-dir <path_to_extracted_folder> --target-dir datasets
   ```

### Option B: Replay-Attack

1. **Visit**: https://www.idiap.ch/en/dataset/replayattack
2. **Register** and download
3. **Extract** the downloaded file
4. **Organize**:
   ```bash
   python scripts/download_dataset.py --dataset replay --source-dir <path_to_extracted_folder> --target-dir datasets
   ```

### Option C: CelebA-Spoof

1. **Visit**: https://mmlab.ie.cuhk.edu.hk/projects/CelebA_Spoof.html
2. **Request access** (requires approval)
3. **Download** and organize manually into:
   - `datasets/real/` - real face images
   - `datasets/spoof/` - spoof face images

### Option D: Test with Synthetic Data (Quick Test)

```bash
cd backend
python model/preprocess_dataset.py synthetic
```

This creates a small synthetic dataset for testing (not for production use).

---

## 🎓 Step 2: Train the Model

Once you have a dataset organized in `datasets/real/` and `datasets/spoof/`:

### Quick Training

```bash
python scripts/train_model.py
```

### Manual Training

```bash
cd backend
python model/train_model.py
```

**Training Details**:
- **Epochs**: 10 (adjustable)
- **Batch size**: 32
- **Time**: ~30-60 minutes depending on dataset size
- **Output**: `models/liveness_model.h5`

**Note**: The system works without a trained model (uses heuristics), but accuracy is much better with a trained model.

---

## 🚀 Step 3: Deploy Backend

### Using Render.com

1. **Sign up**: https://render.com
2. **New Web Service**:
   - Connect GitHub repository
   - Settings:
     - **Name**: `face-liveness-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Deploy** and wait (5-10 min)
4. **Copy your URL**: `https://your-app.onrender.com`

**OR** use the `render.yaml` file - Render will auto-detect it!

### Using Railway.app

1. **Sign up**: https://railway.app
2. **New Project** → Deploy from GitHub
3. **Settings** → Deploy:
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** and get your URL

**OR** use the `railway.json` file - Railway will auto-detect it!

### Update CORS

After deployment, update `backend/main.py`:

```python
allow_origins=[
    "https://your-frontend.vercel.app",  # Add your frontend URL
    "http://localhost:3000"
],
```

Commit and push (auto-redeploys).

---

## 🌐 Step 4: Deploy Frontend

### Using Vercel

1. **Sign up**: https://vercel.com (can use GitHub account)

2. **New Project**:
   - Import GitHub repository
   - Settings:
     - **Framework**: Create React App
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `build`

3. **Environment Variables** (Important!):
   
   Click "Environment Variables" and add:
   
   - **REACT_APP_API_URL**
     - Value: Your backend URL
     - Example: `https://face-liveness-backend.onrender.com`
   
   - **REACT_APP_WS_URL**
     - Value: WebSocket URL (use `wss://`)
     - Example: `wss://face-liveness-backend.onrender.com`
     - ⚠️ **Important**: Use `wss://` not `ws://` for secure WebSocket

4. **Deploy** and wait (2-5 min)

5. **Get your URL**: `https://your-app.vercel.app`

---

## ⚙️ Step 5: Update Environment Variables

### After Deployment

You should have:
- **Backend URL**: `https://your-backend.onrender.com` (or Railway)
- **Frontend URL**: `https://your-frontend.vercel.app`

### Update Frontend (if needed)

Go back to Vercel → Your Project → Settings → Environment Variables:
- Update `REACT_APP_API_URL` with your backend URL
- Update `REACT_APP_WS_URL` with `wss://` version of backend URL

### Update Backend CORS

Edit `backend/main.py`:
```python
allow_origins=[
    "https://your-actual-frontend.vercel.app",  # Your real frontend URL
    "http://localhost:3000"
],
```

Commit and push (auto-redeploys).

---

## ✅ Verification

### Test Backend

Visit: `https://your-backend-url/health`

Should see:
```json
{"status":"healthy","model_loaded":true}
```

### Test Frontend

1. Visit your frontend URL
2. Click "Start Detection"
3. Allow camera permissions
4. Should see:
   - Camera feed
   - Face detection box
   - Real/Spoof result

### Test WebSocket

1. Open browser console (F12)
2. Look for: "WebSocket connected"
3. Should see frame processing

---

## 📋 Checklist

- [ ] Dataset downloaded and organized
- [ ] Model trained (`models/liveness_model.h5` exists)
- [ ] Code pushed to GitHub
- [ ] Backend deployed (Render/Railway)
- [ ] Backend health check works
- [ ] Frontend deployed (Vercel)
- [ ] Environment variables set in Vercel
- [ ] CORS updated in backend
- [ ] Frontend loads correctly
- [ ] Camera access works
- [ ] Detection works end-to-end

---

## 🔧 Troubleshooting

### Dataset Issues

**Problem**: Can't download dataset
- **Solution**: Use synthetic dataset for testing: `python backend/model/preprocess_dataset.py synthetic`

### Training Issues

**Problem**: Training fails
- Check you have images in both `datasets/real/` and `datasets/spoof/`
- Ensure you have enough disk space
- Check Python and TensorFlow versions

**Problem**: Out of memory
- Reduce batch size in `train_model.py`
- Use smaller dataset subset

### Deployment Issues

**Problem**: Backend not starting
- Check logs in Render/Railway dashboard
- Verify all dependencies in `requirements.txt`
- Check Python version

**Problem**: WebSocket not connecting
- Use `wss://` (not `ws://`) in production
- Check CORS settings
- Verify backend supports WebSockets

**Problem**: Camera not working
- Requires HTTPS (production should be fine)
- Check browser permissions
- Test in different browser

---

## 📞 Need Help?

1. Check detailed guides:
   - `DEPLOYMENT_STEPS.md` - Step-by-step deployment
   - `DEPLOYMENT.md` - General deployment info
   - `ARCHITECTURE.md` - System architecture

2. Check logs:
   - Backend: Render/Railway dashboard
   - Frontend: Vercel dashboard
   - Browser: Console (F12)

3. Run diagnostic:
   ```bash
   python scripts/setup_complete.py
   ```

---

## 🎉 Success!

Once everything is working:
- ✅ Backend: `https://your-backend-url`
- ✅ Frontend: `https://your-frontend-url`
- ✅ Model: Trained and deployed
- ✅ System: Fully functional

**Congratulations!** Your Face Liveness Detection System is live! 🚀

