# Backend Setup & Testing Guide

## Prerequisites
- Python 3.8+
- OpenAI API key
- Firebase service account JSON
- (Optional) Pinecone API key for vector DB

## Installation

1. Install dependencies (in progress):
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your credentials:
```env
# Firebase
FIREBASE_CREDENTIALS_PATH=path/to/your/serviceAccountKey.json

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Pinecone (optional)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=interview-assistant

# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Running the Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing the WebSocket Connection

### 1. Test WebSocket Endpoint

Open browser console or use a WebSocket client:

```javascript
// Connect to WebSocket
const sessionId = 'test-session-123';
const ws = new WebSocket(`ws://localhost:8000/ws/interview/${sessionId}`);

ws.onopen = () => {
  console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

### 2. Test Audio Streaming

```javascript
// Capture audio from microphone
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
        // Convert blob to arraybuffer and send
        event.data.arrayBuffer().then(buffer => {
          ws.send(buffer);
        });
      }
    };
    
    // Start recording in 100ms chunks
    mediaRecorder.start(100);
  });
```

### 3. Expected WebSocket Messages

**Transcript Message:**
```json
{
  "type": "transcript",
  "timestamp": 1234567890,
  "data": {
    "text": "Tell me about your experience",
    "speaker": "recruiter",
    "isFinal": true
  }
}
```

**Question Detected:**
```json
{
  "type": "question_detected",
  "timestamp": 1234567890,
  "data": {
    "question": "Tell me about your experience with Python",
    "timestamp": 1234567890
  }
}
```

**Answer Generated:**
```json
{
  "type": "answer_generated",
  "timestamp": 1234567890,
  "data": {
    "questionId": "qa-123456",
    "answer": "I have 5 years of Python experience...",
    "confidence": 0.85,
    "contextUsed": {
      "resumeSection": "Experience > ABC Corp",
      "jdSection": "Required Skills > Python"
    }
  }
}
```

## API Endpoints

### Health Check
```
GET /health
```

### Session Management
```
GET /api/sessions/{session_id}
POST /api/sessions
```

### Resume Upload
```
POST /api/resumes
```

## Troubleshooting

### Dependencies Not Installing
If pip install fails, try installing packages individually:
```bash
pip install fastapi uvicorn
pip install firebase-admin
pip install openai
pip install openai-whisper
```

### Whisper Model Download
First time running will download Whisper model (~140MB for base model):
```python
# This happens automatically on first transcription
# Models: tiny, base, small, medium, large
```

### Firebase Authentication Error
Ensure your service account JSON has these permissions:
- Cloud Firestore: Read/Write
- Cloud Storage: Read/Write

### WebSocket Connection Refused
- Check if backend is running: `http://localhost:8000/health`
- Verify CORS settings in `.env`
- Check frontend is using correct WebSocket URL

### Audio Not Transcribing
- Verify microphone permissions in browser
- Check audio format (WebM/Opus recommended)
- Ensure chunks are being sent (check browser console)
- Verify Whisper model loaded (check backend logs)

## Development Notes

### Current Implementation Status

✅ **Phase 3: Live Interview Engine (70%)**
- Audio processor service
- Transcription service (Whisper)
- Question detector (pattern matching)
- WebSocket connection manager
- Complete WebSocket pipeline in main.py

✅ **Phase 4: AI Answer Generation (60%)**
- Answer generator with GPT-4
- Firebase service for data retrieval
- Resume/JD context extraction
- Follow-up session context support

❌ **TODO:**
- Speaker diarization (Pyannote.audio)
- Resume parsing (PyPDF2/docx)
- Vector DB setup (Pinecone/ChromaDB)
- Session recording to Storage
- Self-learning pipeline

## Architecture

```
Client (Browser)
    ↓ WebSocket connection
Backend (FastAPI)
    ↓ Audio chunks (bytes)
Audio Processor
    ↓ NumPy arrays
Transcription Service (Whisper)
    ↓ Text transcript
Question Detector
    ↓ Detected question
Answer Generator (GPT-4)
    ↓ Personalized answer
Firebase Service
    ↓ Save to Firestore
Client receives answer
```

## Performance Tips

1. **Whisper Model Selection:**
   - `tiny` (39M): Fastest, lowest accuracy
   - `base` (74M): Good balance (recommended)
   - `small` (244M): Better accuracy
   - `medium` (769M): High accuracy, slower
   - `large` (1550M): Best accuracy, very slow

2. **Audio Buffering:**
   - Default: 3 seconds (~30 chunks)
   - Adjust in `main.py`: `BUFFER_SIZE`

3. **GPT-4 Settings:**
   - Temperature: 0.7 (creative but controlled)
   - Max tokens: 300 (concise answers)

## Next Steps

1. Wait for dependencies to finish installing
2. Set up `.env` file with credentials
3. Download Firebase service account JSON
4. Run `python main.py`
5. Test WebSocket connection
6. Connect frontend and test end-to-end
