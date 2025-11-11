# Project Architecture & Structure

## 📁 Proposed Project Structure

```
Real-Time-AI-Interview-Assistant/
├── frontend/                          # Next.js mobile-first web app
│   ├── app/                          # Next.js 14 App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx              # Dashboard home
│   │   │   ├── interview/
│   │   │   │   ├── page.tsx          # Interview session
│   │   │   │   └── [sessionId]/      # Session details
│   │   │   ├── history/
│   │   │   └── settings/
│   │   ├── api/                      # API routes (optional)
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/                       # Shadcn UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   ├── audio/
│   │   │   ├── RecordButton.tsx
│   │   │   ├── AudioVisualizer.tsx
│   │   │   ├── DeviceSelector.tsx
│   │   │   └── VolumeIndicator.tsx
│   │   ├── interview/
│   │   │   ├── TranscriptDisplay.tsx
│   │   │   ├── ResponseStreaming.tsx
│   │   │   ├── QuestionCard.tsx
│   │   │   └── Timer.tsx
│   │   ├── session/
│   │   │   ├── SessionSummary.tsx
│   │   │   ├── SessionHistory.tsx
│   │   │   └── ExportDialog.tsx
│   │   └── layout/
│   │       ├── Navbar.tsx
│   │       └── Sidebar.tsx
│   ├── hooks/
│   │   ├── useAudioRecorder.ts
│   │   ├── useWebSocket.ts
│   │   ├── useTranscription.ts
│   │   ├── useLLMStream.ts
│   │   ├── useSession.ts
│   │   └── useAuth.ts
│   ├── lib/
│   │   ├── api-client.ts             # Axios instance
│   │   ├── websocket.ts              # WebSocket manager
│   │   ├── firebase.ts               # Firebase client
│   │   └── utils.ts
│   ├── types/
│   │   ├── audio.ts
│   │   ├── session.ts
│   │   └── user.ts
│   ├── public/
│   ├── styles/
│   │   └── globals.css
│   ├── .env.local
│   ├── next.config.js
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── backend/                           # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app
│   │   ├── config.py                 # Configuration
│   │   ├── dependencies.py           # Shared dependencies
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── audio.py
│   │   │           ├── transcription.py
│   │   │           ├── llm.py
│   │   │           ├── sessions.py
│   │   │           └── profiles.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── audio_transcriber.py  # Whisper integration
│   │   │   ├── unified_llm_client.py # Groq + Ollama
│   │   │   ├── ollama_client.py
│   │   │   ├── audio_device_util.py
│   │   │   ├── response_quality.py
│   │   │   └── session_manager.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── transcript.py
│   │   │   └── profile.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # Pydantic models
│   │   │   ├── session.py
│   │   │   ├── audio.py
│   │   │   └── llm.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── firebase_service.py   # Firestore, Storage, Auth
│   │   │   ├── vertex_ai_service.py  # Google Cloud Vertex AI
│   │   │   ├── whisper_service.py
│   │   │   ├── llm_service.py
│   │   │   └── export_service.py     # PDF/JSON export
│   │   ├── websockets/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py            # Connection manager
│   │   │   ├── transcription.py
│   │   │   └── llm_stream.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   ├── metrics.py            # Prometheus metrics
│   │   │   └── encryption.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── cors.py
│   │       └── rate_limit.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── test_audio_transcriber.py
│   │   │   ├── test_llm_client.py
│   │   │   └── test_session_manager.py
│   │   ├── integration/
│   │   │   ├── test_api_endpoints.py
│   │   │   └── test_websockets.py
│   │   └── e2e/
│   │       └── test_interview_flow.py
│   ├── alembic/                      # DB migrations (if using SQL)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── pyproject.toml
│
├── mobile/                            # React Native app (Phase 5)
│   ├── app/                          # Expo Router
│   ├── components/
│   ├── hooks/
│   ├── services/
│   ├── app.json
│   └── package.json
│
├── infrastructure/                    # IaC and deployment
│   ├── terraform/                    # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── kubernetes/                   # K8s manifests (if scaling)
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── docker-compose.yml            # Local development
│   └── render.yaml                   # Render deployment config
│
├── scripts/                           # Utility scripts
│   ├── setup_dev.sh                  # Development environment setup
│   ├── run_tests.sh
│   ├── deploy.sh
│   └── migrate_data.py
│
├── docs/                              # Documentation
│   ├── api/
│   │   └── openapi.yaml              # API specification
│   ├── architecture/
│   │   ├── diagrams/
│   │   └── decisions/                # ADRs
│   ├── guides/
│   │   ├── setup.md
│   │   ├── deployment.md
│   │   └── contributing.md
│   └── user-guide.md
│
├── profiles/                          # User profiles (existing)
│   ├── README.md
│   └── [username]/
│       └── profile.py
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # CI/CD pipeline
│   │   ├── deploy-frontend.yml
│   │   └── deploy-backend.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitignore
├── .env.example
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── ROADMAP.md                         # This file
└── RULES.md                           # Development guidelines
```

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Mobile Web   │  │  Desktop Web │  │  React Native App    │ │
│  │  (Next.js)    │  │  (Next.js)   │  │  (Future - Phase 5)  │ │
│  └───────┬───────┘  └──────┬───────┘  └──────────┬───────────┘ │
└──────────┼──────────────────┼──────────────────────┼─────────────┘
           │                  │                      │
           │          HTTPS / WebSocket              │
           │                  │                      │
┌──────────┼──────────────────┼──────────────────────┼─────────────┐
│          │           API Gateway / Load Balancer   │             │
│          └──────────────────┬──────────────────────┘             │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │              FastAPI Backend (Python 3.11+)             │    │
│  │                                                          │    │
│  │  ┌────────────┐  ┌──────────────┐  ┌────────────────┐  │    │
│  │  │  Auth API  │  │  Audio API   │  │  Session API   │  │    │
│  │  └─────┬──────┘  └──────┬───────┘  └────────┬───────┘  │    │
│  │        │                │                    │          │    │
│  │  ┌─────┴────────────────┴────────────────────┴───────┐  │    │
│  │  │         WebSocket Manager (Real-time)            │  │    │
│  │  │  ┌──────────────┐    ┌────────────────────────┐  │  │    │
│  │  │  │ Transcription│    │  LLM Response Stream   │  │  │    │
│  │  │  │   Stream     │    │  (Token-by-token)      │  │  │    │
│  │  │  └──────────────┘    └────────────────────────┘  │  │    │
│  │  └──────────────────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
           │                  │                      │
┌──────────┼──────────────────┼──────────────────────┼─────────────┐
│          │          External Services              │             │
│  ┌───────▼────────┐ ┌──────▼───────┐  ┌──────────▼──────────┐   │
│  │    Firebase    │ │   Whisper    │  │  Google Cloud       │   │
│  │                │ │   (OpenAI)   │  │  Vertex AI          │   │
│  │  ┌──────────┐  │ │              │  │  ┌──────────────┐   │   │
│  │  │Firestore │  │ │ Audio→Text   │  │  │   Groq API   │   │   │
│  │  │(Database)│  │ │              │  │  │  (Primary)   │   │   │
│  │  └──────────┘  │ │              │  │  └──────────────┘   │   │
│  │  ┌──────────┐  │ └──────────────┘  │  ┌──────────────┐   │   │
│  │  │ Storage  │  │                   │  │ Ollama Local │   │   │
│  │  │ (Audio)  │  │                   │  │  (Fallback)  │   │   │
│  │  └──────────┘  │                   │  └──────────────┘   │   │
│  │  ┌──────────┐  │                   └─────────────────────┘   │
│  │  │   Auth   │  │                                              │
│  │  └──────────┘  │                                              │
│  └────────────────┘                                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Interview Session Flow

```
1. User Authentication
   User → Frontend → Firebase Auth → Backend → Session Created

2. Audio Recording
   Microphone → Browser Audio API → WebSocket → Backend Buffer

3. Real-Time Transcription
   Audio Buffer → Whisper Service → Transcription Stream → Frontend Display

4. LLM Response Generation
   Transcription → Context Builder → Groq/Ollama → Token Stream → Frontend

5. Session Persistence
   Q&A Pair → Backend → Firebase Firestore → Session Updated

6. Export
   User Request → Backend → Generate PDF/JSON → Download
```

### Detailed Flow Diagram

```
┌──────────┐
│  User    │
│ (Mobile) │
└────┬─────┘
     │ 1. Click "Start Interview"
     ▼
┌────────────────┐
│   Frontend     │
│  - Select mic  │
│  - Choose      │
│    profile     │
└────┬───────────┘
     │ 2. POST /api/v1/sessions/create
     │    {userId, profileId, jobDescription}
     ▼
┌────────────────┐
│    Backend     │
│  - Validate    │
│  - Create ID   │
└────┬───────────┘
     │ 3. Save to Firestore
     ▼
┌────────────────┐
│   Firebase     │
│  sessions/{id} │
└────┬───────────┘
     │ 4. Return sessionId
     ▼
┌────────────────┐
│   Frontend     │
│  - Show UI     │
│  - Press to    │
│    record      │
└────┬───────────┘
     │ 5. WebSocket connect
     │    /ws/transcribe?session_id=xxx
     ▼
┌────────────────┐
│   Backend      │
│  - Accept WS   │
│  - Load model  │
└────┬───────────┘
     │ 6. Stream audio chunks
     │    {audioData: base64}
     ▼
┌────────────────┐
│  Whisper       │
│  - Transcribe  │
│  - Detect lang │
└────┬───────────┘
     │ 7. Partial transcripts
     │    {text: "Tell me about...", isFinal: false}
     ▼
┌────────────────┐
│   Frontend     │
│  - Display     │
│    text        │
└────┬───────────┘
     │ 8. User stops recording
     │    Final transcript sent
     ▼
┌────────────────┐
│   Backend      │
│  - Build       │
│    context     │
│  - Format      │
│    prompt      │
└────┬───────────┘
     │ 9. POST to Groq/Ollama
     │    {prompt, model, stream: true}
     ▼
┌────────────────┐
│  Groq API      │
│  - Generate    │
│  - Stream      │
│    tokens      │
└────┬───────────┘
     │ 10. Token stream
     │     {delta: "I", finish: false}
     │     {delta: " worked", finish: false}
     │     {delta: " on", finish: true}
     ▼
┌────────────────┐
│   Backend      │
│  - Forward to  │
│    frontend    │
└────┬───────────┘
     │ 11. WebSocket /ws/llm-stream
     ▼
┌────────────────┐
│   Frontend     │
│  - Append      │
│    tokens      │
│  - Display     │
└────┬───────────┘
     │ 12. Response complete
     │     Save Q&A
     ▼
┌────────────────┐
│   Backend      │
│  - POST to     │
│    Firestore   │
└────┬───────────┘
     │ 13. Update session
     ▼
┌────────────────┐
│   Firebase     │
│  sessions/{id} │
│    questions[] │
└────────────────┘
```

---

## 🗄️ Database Schema (Firestore)

### Collections Structure

```javascript
// users collection
users/{userId} = {
  email: string,
  displayName: string,
  photoURL: string,
  createdAt: timestamp,
  settings: {
    preferredLLM: "groq" | "ollama",
    audioDevice: string,
    language: string,
    voiceId: string | null
  },
  subscription: {
    tier: "free" | "pro",
    expiresAt: timestamp | null
  }
}

// profiles subcollection
users/{userId}/profiles/{profileId} = {
  name: string,
  role: string,
  yearsExperience: number,
  skills: string[],
  industry: string,
  context: string, // encrypted
  createdAt: timestamp,
  updatedAt: timestamp
}

// sessions collection
sessions/{sessionId} = {
  userId: string,
  profileId: string,
  jobDescription: string, // encrypted
  status: "active" | "completed" | "abandoned",
  createdAt: timestamp,
  completedAt: timestamp | null,
  duration: number, // seconds
  questionCount: number,
  metadata: {
    llmProvider: "groq" | "ollama",
    model: string,
    language: string
  }
}

// transcripts subcollection
sessions/{sessionId}/transcripts/{transcriptId} = {
  questionNumber: number,
  question: string,
  answer: string,
  timestamp: timestamp,
  metrics: {
    responseTime: number, // seconds
    wordCount: number,
    confidence: number, // 0-1
    qualityScore: number | null // 0-100
  },
  audioUrl: string | null // Firebase Storage URL
}

// analytics collection (aggregated data)
analytics/{date} = {
  totalSessions: number,
  totalUsers: number,
  averageSessionDuration: number,
  topRoles: string[],
  llmProviderUsage: {
    groq: number,
    ollama: number
  }
}
```

### Firestore Indexes

```javascript
// Compound indexes for efficient queries
sessions
  - userId (ASC), createdAt (DESC)
  - status (ASC), createdAt (DESC)

transcripts (within session)
  - questionNumber (ASC)
  - timestamp (ASC)

profiles (within user)
  - role (ASC), createdAt (DESC)
```

---

## 🔌 API Endpoints Reference

### Authentication

```
POST   /api/v1/auth/signup
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me
```

### Audio

```
POST   /api/v1/audio/upload
GET    /api/v1/audio/{audio_id}
DELETE /api/v1/audio/{audio_id}
GET    /api/v1/audio/devices
```

### Transcription

```
POST   /api/v1/transcribe
WS     /ws/transcribe
GET    /api/v1/transcripts/{transcript_id}
```

### LLM

```
POST   /api/v1/llm/generate
WS     /ws/llm-stream
POST   /api/v1/llm/interrupt
GET    /api/v1/llm/models
```

### Sessions

```
POST   /api/v1/sessions
GET    /api/v1/sessions
GET    /api/v1/sessions/{session_id}
PUT    /api/v1/sessions/{session_id}
DELETE /api/v1/sessions/{session_id}
POST   /api/v1/sessions/{session_id}/export
```

### Profiles

```
GET    /api/v1/profiles
POST   /api/v1/profiles
GET    /api/v1/profiles/{profile_id}
PUT    /api/v1/profiles/{profile_id}
DELETE /api/v1/profiles/{profile_id}
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Shadcn UI
- **State Management**: Zustand / React Context
- **Forms**: React Hook Form + Zod
- **API Client**: Axios
- **WebSocket**: native WebSocket API
- **Audio**: Web Audio API, MediaRecorder API
- **Charts**: Recharts
- **PDF Generation**: jsPDF

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Async**: asyncio, httpx
- **Validation**: Pydantic v2
- **Database**: Firebase Firestore
- **Storage**: Firebase Storage
- **Authentication**: Firebase Auth
- **LLM**: Groq API, Ollama
- **Transcription**: OpenAI Whisper (large)
- **WebSocket**: FastAPI WebSocket
- **Monitoring**: Prometheus, Sentry
- **Logging**: structlog

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render / Railway
- **Database**: Firebase (Firestore)
- **Storage**: Firebase Storage
- **AI/ML**: Google Cloud Vertex AI
- **CDN**: Vercel Edge Network
- **CI/CD**: GitHub Actions
- **Monitoring**: Grafana Cloud

---

## 📊 Performance Targets

| Metric | Target | Priority |
|--------|--------|----------|
| API Response Time (p95) | <100ms | HIGH |
| WebSocket Latency | <50ms | HIGH |
| Transcription Delay | <2s | HIGH |
| LLM First Token | <500ms | MEDIUM |
| Frontend Load Time | <2s | HIGH |
| Time to Interactive | <3s | MEDIUM |
| Uptime | >99.9% | HIGH |
| Error Rate | <0.1% | HIGH |

---

## 🔒 Security Measures

1. **Authentication**: Firebase JWT tokens
2. **Authorization**: Row-level security in Firestore
3. **Encryption**: AES-256 for sensitive fields
4. **HTTPS**: Enforced on all endpoints
5. **Rate Limiting**: 100 req/min per user
6. **Input Validation**: Pydantic schemas
7. **CORS**: Whitelisted origins only
8. **API Keys**: Environment variables, never committed
9. **Audit Logging**: All data access logged
10. **Data Retention**: 30-day policy for audio files

---

## 📈 Scalability Plan

### Horizontal Scaling
- Multiple FastAPI instances behind load balancer
- Stateless backend (session in Firestore)
- WebSocket sticky sessions

### Database Scaling
- Firestore auto-scales
- Implement caching (Redis) for hot data
- Aggregate analytics to reduce reads

### Cost Optimization
- Use Groq for speed (cost-effective)
- Fallback to Ollama (local, free)
- Compress audio before upload
- Lifecycle policies for Firebase Storage

---

## 🧪 Testing Strategy

### Unit Tests
- All service functions
- Utility functions
- Target: >80% coverage

### Integration Tests
- API endpoints
- WebSocket connections
- Firebase interactions

### E2E Tests
- Complete interview flow
- Export functionality
- Multi-device responsiveness

### Performance Tests
- Load testing (Apache JMeter)
- Stress testing (Locust)
- Target: 100 concurrent users

---

## 📚 Documentation Standards

- **Code Comments**: For complex logic only
- **Docstrings**: All public functions/classes
- **API Docs**: OpenAPI 3.0 specification
- **Architecture**: Diagrams in docs/architecture/
- **ADRs**: Document all major decisions
- **User Guide**: Comprehensive end-user docs
- **README**: Setup, usage, contribution

---

This architecture supports the full roadmap from Phase 1 to Phase 5, with clear separation of concerns, scalability, and maintainability built in from the start.
