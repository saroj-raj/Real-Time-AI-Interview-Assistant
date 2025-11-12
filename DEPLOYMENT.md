# Deployment Guide

## Overview
This guide covers deploying the Real-Time AI Interview Assistant with:
- **Frontend**: Vercel (Next.js)
- **Backend**: Render or Railway (FastAPI + Groq)

---

## Prerequisites

1. **Groq API Key**: Get from [console.groq.com](https://console.groq.com)
2. **Firebase Project**: Create at [firebase.google.com](https://firebase.google.com)
3. **GitHub Repository**: Push your code to GitHub
4. **Accounts**: 
   - [Vercel](https://vercel.com) (Frontend)
   - [Render](https://render.com) or [Railway](https://railway.app) (Backend)

---

## Part 1: Deploy Backend (Render)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Real-Time-AI-Interview-Assistant.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `interview-assistant-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   LLM_TEMPERATURE=0.7
   LLM_MAX_TOKENS=300
   WHISPER_MODEL=base
   DEBUG=False
   ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL**: `https://interview-assistant-backend.onrender.com`

---

## Part 2: Deploy Frontend (Vercel)

### Step 1: Deploy on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. **Add Environment Variables**:
   ```
   NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-app.appspot.com
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
   NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
   NEXT_PUBLIC_API_URL=https://interview-assistant-backend.onrender.com
   ```

5. Click **"Deploy"**
6. Wait 2-3 minutes
7. **Your app is live!** `https://your-app.vercel.app`

### Step 2: Update Backend CORS

Go back to Render and update the `ALLOWED_ORIGINS` environment variable:
```
ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## Part 3: Firebase Setup

### Step 1: Get Firebase Config

1. Go to [console.firebase.google.com](https://console.firebase.google.com)
2. Select your project
3. Go to **Project Settings** → **General**
4. Scroll to **"Your apps"** → **Web app**
5. Copy all config values

### Step 2: Enable Google Sign-In

1. In Firebase Console, go to **Authentication**
2. Click **"Get Started"**
3. Go to **"Sign-in method"** tab
4. Enable **"Google"** provider
5. Add your Vercel domain to authorized domains

### Step 3: Create Service Account (Optional for full features)

1. Go to **Project Settings** → **Service Accounts**
2. Click **"Generate new private key"**
3. Save JSON file securely
4. Add to Render as secret file or environment variable

---

## Alternative: Deploy Backend on Railway

### Quick Deploy on Railway

1. Go to [railway.app/new](https://railway.app/new)
2. Click **"Deploy from GitHub repo"**
3. Select your repository
4. Configure:
   - **Root Directory**: `/backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables (same as Render)
6. Deploy and copy public URL

---

## Testing Deployment

### 1. Test Backend
```bash
curl https://your-backend.onrender.com/
```

Expected response:
```json
{"message": "Real-Time Interview Assistant API", "status": "running"}
```

### 2. Test Frontend
1. Open `https://your-app.vercel.app`
2. Sign up with email or Google
3. Upload resume and JD
4. Start interview session
5. Test microphone and answer generation

---

## Troubleshooting

### Backend Issues

**Cold starts (Render free tier)**:
- First request takes 30-60 seconds
- Keep alive with scheduled pings

**Whisper model loading**:
- Add to Dockerfile: `RUN python -c "import whisper; whisper.load_model('base')"`

**Memory errors**:
- Upgrade to paid plan or use smaller Whisper model (`tiny`)

### Frontend Issues

**Firebase auth not working**:
- Check authorized domains in Firebase Console
- Verify environment variables

**WebSocket connection failed**:
- Update `NEXT_PUBLIC_API_URL` with correct backend URL
- Check CORS settings on backend

### Performance

**Slow answer generation**:
- Groq is fast (usually < 2 seconds)
- Check network latency

**Audio transcription lag**:
- Use smaller Whisper model (`base` or `tiny`)
- Reduce audio chunk size

---

## Cost Estimates

### Free Tier (Recommended for testing)
- **Groq**: Free tier with limits
- **Vercel**: Free for personal projects
- **Render**: Free tier with cold starts
- **Firebase**: Free tier (Spark plan)

**Total**: $0/month for light usage

### Production Tier
- **Groq**: Pay-as-you-go
- **Vercel**: $20/month (Pro)
- **Render**: $7-25/month (Starter/Standard)
- **Firebase**: $25-50/month (Blaze plan)

**Total**: ~$50-100/month

---

## Security Checklist

- [ ] Keep API keys in environment variables (never commit)
- [ ] Enable Firebase Security Rules
- [ ] Use HTTPS only
- [ ] Set proper CORS origins
- [ ] Enable rate limiting
- [ ] Monitor usage and costs
- [ ] Set up error tracking (Sentry)
- [ ] Enable authentication on all endpoints

---

## Next Steps

1. **Custom Domain**: Add your domain in Vercel
2. **Analytics**: Add PostHog or Google Analytics
3. **Monitoring**: Set up Sentry for error tracking
4. **CDN**: Vercel handles this automatically
5. **Backups**: Enable Firestore backups
6. **CI/CD**: Automatic deployments on push

---

## Support

If you encounter issues:
1. Check logs in Render/Vercel dashboard
2. Test locally first
3. Verify all environment variables
4. Check Firebase quotas
5. Review CORS configuration

**Your interview assistant is now live!** 🚀
