# Setup Instructions

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env and add your credentials:
# - FIREBASE_CREDENTIALS_PATH: Path to your Firebase service account JSON
# - OPENAI_API_KEY: Your OpenAI API key

# Run the server
python main.py
```

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Copy environment template (if needed)
# Edit .env.local with your Firebase config

# Run development server
npm run dev
```

### 3. Open Browser

Navigate to `http://localhost:3000`

---

## Detailed Setup

### Backend (Python/FastAPI)

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Dependencies
```bash
cd backend
pip install -r requirements.txt
```

This installs:
- **FastAPI**: Web framework for API
- **Uvicorn**: ASGI server
- **WebSockets**: Real-time communication
- **Firebase Admin**: Database & storage
- **OpenAI**: GPT-4 for answer generation
- **Whisper**: Speech-to-text transcription
- **Pyannote.audio**: Speaker diarization (TODO)
- **LangChain**: RAG framework
- **Pinecone/ChromaDB**: Vector database (TODO)
- **PyPDF2/python-docx**: Resume parsing (TODO)

#### Environment Variables

Create `backend/.env`:

```env
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
OPENAI_API_KEY=sk-your-key-here
CORS_ORIGINS=http://localhost:3000
```

**Get Firebase Credentials:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings > Service Accounts
4. Click "Generate New Private Key"
5. Save JSON as `backend/serviceAccountKey.json`

**Get OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys
4. Create new secret key
5. Copy and paste into `.env`

#### Run Backend

```bash
cd backend
python main.py
```

Or with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verify:**
- Open `http://localhost:8000/health`
- Should see: `{"status": "healthy"}`

---

### Frontend (Next.js/React)

#### Prerequisites
- Node.js 18 or higher
- npm (comes with Node.js)

#### Dependencies
```bash
cd frontend
npm install
```

This installs:
- **Next.js 14**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Firebase**: Authentication & database
- **Zustand**: State management
- **React Hook Form**: Form handling
- **Radix UI**: Component primitives

#### Firebase Config

Frontend Firebase config is already in the code:

`frontend/lib/firebase.ts` contains the Firebase client config.

You may need to update it with your own Firebase project settings:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings > General
4. Scroll to "Your apps" > Web app
5. Copy the config object
6. Update `frontend/lib/firebase.ts`

#### Run Frontend

```bash
cd frontend
npm run dev
```

**Verify:**
- Open `http://localhost:3000`
- Should see login page
- No errors in browser console

---

## Testing the Complete Flow

### 1. Create Account
- Go to `http://localhost:3000/login`
- Click "Sign up"
- Enter email/password or use Google OAuth
- Should redirect to dashboard

### 2. Upload Resume
- Click "Upload Resume"
- Select PDF, DOCX, or TXT file
- Wait for upload
- Resume appears in list

### 3. Add Job Description
- Click "Add Job Description"
- Fill in company name, role, description
- Click "Save"
- JD appears in list

### 4. Start Interview
- Select resume and JD
- Click "Quick Start Interview"
- Configure company/role
- Click "Start Interview"

### 5. Live Interview
- Click "Start Listening"
- Allow microphone access
- Speak: "Tell me about your experience with Python"
- Wait for transcription
- Wait for answer generation
- Answer appears in card

### 6. Verify Data
- Check Firebase Console
- Go to Firestore
- Check `sessions/{sessionId}`
- Verify transcripts and Q&A saved

---

## Troubleshooting

### Backend Won't Start

**Error: ModuleNotFoundError**
```
Solution: pip install -r requirements.txt
```

**Error: Firebase credentials not found**
```
Solution: 
1. Download serviceAccountKey.json
2. Place in backend/ folder
3. Update FIREBASE_CREDENTIALS_PATH in .env
```

**Error: OpenAI API key invalid**
```
Solution:
1. Verify key in .env
2. Check for extra spaces
3. Ensure key starts with "sk-"
4. Regenerate key if needed
```

### Frontend Won't Start

**Error: Module not found**
```
Solution: npm install
```

**Error: Firebase config error**
```
Solution:
1. Check frontend/lib/firebase.ts
2. Verify Firebase project settings
3. Ensure all config fields present
```

### WebSocket Connection Failed

**Error: WebSocket connection to 'ws://localhost:8000' failed**
```
Solution:
1. Ensure backend is running
2. Check CORS_ORIGINS in backend/.env
3. Verify port 8000 not in use
4. Check firewall settings
```

### Microphone Not Working

**Error: Permission denied**
```
Solution:
1. Allow mic in browser settings
2. Use HTTPS in production
3. Check browser compatibility
4. Test in Chrome (best support)
```

### Transcription Not Working

**Error: No transcript appearing**
```
Solution:
1. Check backend logs for errors
2. Verify Whisper model downloaded
3. Speak louder/clearer
4. Wait full 3 seconds
5. Check audio buffer size
```

### No Questions Detected

**Error: Questions not highlighted**
```
Solution:
1. Use question words (what, how, tell me)
2. Check question_detector.py patterns
3. Lower confidence threshold
4. Verify transcript is accurate
```

### Answer Not Generating

**Error: No answer appears**
```
Solution:
1. Check OpenAI API key
2. Verify credits/billing
3. Check resume uploaded
4. Verify JD exists
5. Check backend logs
```

---

## Production Deployment

### Backend Deployment

**Option 1: Render**
1. Push code to GitHub
2. Go to [Render Dashboard](https://render.com/)
3. New > Web Service
4. Connect GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python main.py`
7. Add environment variables
8. Deploy

**Option 2: Railway**
1. Push code to GitHub
2. Go to [Railway Dashboard](https://railway.app/)
3. New Project > Deploy from GitHub
4. Select repo
5. Add environment variables
6. Deploy

### Frontend Deployment

**Vercel (Recommended for Next.js):**
1. Push code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/)
3. New Project
4. Import GitHub repo
5. Configure:
   - Framework: Next.js
   - Root Directory: frontend
   - Build Command: `npm run build`
   - Output Directory: `.next`
6. Add environment variables (if any)
7. Deploy

**Update CORS:**
After deployment, update `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

---

## Cost Estimates

### OpenAI API
- **Whisper**: ~$0.006/minute of audio
- **GPT-4 Turbo**: ~$0.01/1K tokens (~$0.003 per answer)
- **Example**: 30-min interview, 20 questions = $0.24

### Firebase
- **Free Tier**: 
  - 1 GB storage
  - 10 GB data transfer
  - 50K document reads/day
  - 20K document writes/day
- **Typical Usage**: Free for personal use, ~$5-10/month for 100+ users

### Pinecone (Optional)
- **Starter**: $70/month (1M vectors)
- **Free Alternative**: Use ChromaDB (local)

---

## Next Steps

1. ✅ Complete backend implementation
2. ✅ Complete frontend integration
3. ⏳ Test end-to-end flow
4. ⏳ Add speaker diarization
5. ⏳ Implement resume parsing
6. ⏳ Set up vector database
7. ⏳ Build self-learning pipeline
8. ⏳ Deploy to production

---

## Support

**Issues:**
- Check `TESTING.md` for comprehensive testing guide
- Review backend logs: `backend/logs/`
- Check browser console for frontend errors
- Verify Firebase rules and permissions

**Documentation:**
- Backend API: `backend/README.md`
- Testing Guide: `TESTING.md`
- Original Requirements: `README.md`

---

## Quick Reference

**Start Backend:**
```bash
cd backend && python main.py
```

**Start Frontend:**
```bash
cd frontend && npm run dev
```

**Test Health:**
```bash
curl http://localhost:8000/health
```

**View Logs:**
```bash
tail -f backend/logs/app.log
```

**Reset Database:**
- Go to Firebase Console
- Firestore > Delete collections
- Storage > Delete files
