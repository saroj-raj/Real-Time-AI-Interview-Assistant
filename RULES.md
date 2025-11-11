# Copilot Development Guidelines for Real-Time AI Interview Assistant

## 1. General Code Quality

### 1.1 Clarity
- Write self-documenting code with descriptive variable and function names
- Add comments for complex logic, algorithms, or business rules
- Use docstrings for all functions, classes, and modules
- Keep functions focused on single responsibility (max 50 lines)

### 1.2 Consistency
- **Python**: Follow PEP 8 style guide
- **TypeScript/JavaScript**: Follow Airbnb style guide
- Use 4 spaces for Python, 2 spaces for TypeScript/JavaScript
- Consistent naming conventions:
  - `snake_case` for Python functions/variables
  - `camelCase` for TypeScript/JavaScript functions/variables
  - `PascalCase` for classes and components
  - `UPPER_SNAKE_CASE` for constants

### 1.3 Modularity
- Break down large functions into smaller, reusable utilities
- Create shared utilities in `/utils` or `/lib` directories
- Follow DRY (Don't Repeat Yourself) principle
- Use composition over inheritance
- Separate concerns: UI, business logic, data access

### 1.4 Error Handling
- Always wrap external calls (API, DB, file I/O) in try-catch blocks
- Use specific exception types, avoid bare `except:`
- Log errors with context (user ID, session ID, timestamp)
- Provide user-friendly error messages
- Implement retry logic for transient failures (network, API limits)
- Example:
  ```python
  try:
      result = await api_call()
  except HTTPException as e:
      logger.error(f"API call failed: {e}, session_id={session_id}")
      raise HTTPException(status_code=503, detail="Service temporarily unavailable")
  except Exception as e:
      logger.critical(f"Unexpected error: {e}")
      raise
  ```

### 1.5 Testing
- **Unit Tests**: Test individual functions in isolation
  - Use `pytest` for Python, `Jest` for TypeScript
  - Target >80% code coverage
  - Mock external dependencies
- **Integration Tests**: Test API endpoints end-to-end
  - Use `httpx` for FastAPI testing
  - Test happy paths and error cases
- **E2E Tests**: Test user workflows with Playwright
  - Critical user journeys (signup, record, export)
- Test naming: `test_<function>_<scenario>_<expected_result>`

---

## 2. Frontend (Mobile-First)

### 2.1 Responsive Design
- **Mobile-first approach**: Design for 375px width first
- Use CSS Grid for layouts, Flexbox for components
- Breakpoints:
  ```css
  /* Mobile: default */
  @media (min-width: 768px) { /* Tablet */ }
  @media (min-width: 1024px) { /* Desktop */ }
  ```
- Test on real devices (iOS Safari, Android Chrome)
- Use `rem` units for scalability
- Touch targets: minimum 44x44px (iOS), 48x48px (Android)

### 2.2 Minimalist UI
- Follow Material Design or Apple HIG principles
- Limit color palette (3-5 colors max)
- Use system fonts for performance
- Avoid animations >300ms
- Progressive disclosure: show advanced options only when needed
- Accessibility: WCAG 2.1 AA compliance
  - Proper heading hierarchy (h1 → h2 → h3)
  - ARIA labels for interactive elements
  - Keyboard navigation support
  - Color contrast ratio >4.5:1

### 2.3 Real-Time Feedback
- Use WebSocket for bidirectional communication
- Display connection status indicator
- Optimistic UI updates (update immediately, rollback on error)
- Loading states for all async actions
- Show progress for long operations (upload, transcription)
- Example WebSocket hook:
  ```typescript
  const useWebSocket = (url: string) => {
    const [isConnected, setIsConnected] = useState(false);
    const [messages, setMessages] = useState([]);
    
    useEffect(() => {
      const ws = new WebSocket(url);
      ws.onopen = () => setIsConnected(true);
      ws.onmessage = (event) => {
        setMessages(prev => [...prev, JSON.parse(event.data)]);
      };
      ws.onerror = () => setIsConnected(false);
      return () => ws.close();
    }, [url]);
    
    return { isConnected, messages };
  };
  ```

### 2.4 Performance
- Lazy load components with `React.lazy()`
- Code splitting by route
- Optimize images: WebP format, responsive sizes
- Debounce user input (search, filters)
- Virtualize long lists (react-window)
- Measure with Lighthouse (target >90 score)

---

## 3. Backend (FastAPI + Firebase + Google Cloud Vertex AI)

### 3.1 FastAPI Best Practices
- **Async/Await**: Use for all I/O operations
  ```python
  @app.post("/transcribe")
  async def transcribe_audio(file: UploadFile):
      audio_data = await file.read()
      result = await whisper_service.transcribe(audio_data)
      return result
  ```
- **Dependency Injection**: Use FastAPI's `Depends()`
  ```python
  def get_current_user(token: str = Depends(oauth2_scheme)):
      return verify_token(token)
  
  @app.get("/sessions")
  async def get_sessions(user: User = Depends(get_current_user)):
      return await db.get_user_sessions(user.id)
  ```
- **Pydantic Models**: Validate all input/output
  ```python
  class SessionCreate(BaseModel):
      user_id: str
      job_description: str
      profile_id: Optional[str] = None
  ```
- **Background Tasks**: Use for non-blocking operations
  ```python
  @app.post("/upload")
  async def upload_audio(
      file: UploadFile,
      background_tasks: BackgroundTasks
  ):
      background_tasks.add_task(process_audio, file)
      return {"status": "processing"}
  ```

### 3.2 Security
- **HTTPS Only**: Enforce in production
- **CORS**: Whitelist frontend origins
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://yourdomain.com"],
      allow_credentials=True,
      allow_methods=["GET", "POST"],
      allow_headers=["*"],
  )
  ```
- **Rate Limiting**: Prevent abuse
  ```python
  from slowapi import Limiter
  limiter = Limiter(key_func=lambda: request.client.host)
  
  @app.get("/api/endpoint")
  @limiter.limit("10/minute")
  async def endpoint():
      pass
  ```
- **Input Validation**: Never trust user input
- **SQL Injection Prevention**: Use parameterized queries
- **Firebase Authentication**: Verify tokens on every request
  ```python
  from firebase_admin import auth
  
  async def verify_firebase_token(token: str):
      try:
          decoded_token = auth.verify_id_token(token)
          return decoded_token['uid']
      except Exception:
          raise HTTPException(status_code=401)
  ```

### 3.3 Data Storage
- **Firebase Firestore**:
  - Use subcollections for nested data
  - Denormalize for read performance
  - Use batch writes for multiple updates
  - Example:
    ```python
    from firebase_admin import firestore
    
    db = firestore.client()
    session_ref = db.collection('sessions').document(session_id)
    session_ref.set({
        'user_id': user_id,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'questions': []
    })
    ```
- **Encryption**: Encrypt sensitive fields
  ```python
  from cryptography.fernet import Fernet
  
  cipher = Fernet(ENCRYPTION_KEY)
  encrypted_data = cipher.encrypt(sensitive_data.encode())
  ```
- **Firestore Security Rules**:
  ```javascript
  rules_version = '2';
  service cloud.firestore {
    match /databases/{database}/documents {
      match /sessions/{sessionId} {
        allow read, write: if request.auth.uid == resource.data.user_id;
      }
    }
  }
  ```

### 3.4 Model Inference
- **Google Cloud Vertex AI**:
  - Use Groq for primary inference (fast, cloud)
  - Fallback to Ollama (local, private)
  - Implement circuit breaker pattern
  - Cache common prompts in Redis
  - Example:
    ```python
    from google.cloud import aiplatform
    
    async def generate_response(prompt: str):
        try:
            # Try Groq first
            response = await groq_client.generate(prompt)
        except Exception as e:
            logger.warning(f"Groq failed: {e}, falling back to Ollama")
            response = await ollama_client.generate(prompt)
        return response
    ```

---

## 4. Real-Time Audio Processing

### 4.1 Low-Latency
- Target: <100ms end-to-end latency
- Use streaming audio (don't wait for full recording)
- WebSocket for real-time transcription
- Optimize Whisper model size:
  - Use `base` model for speed (<1s)
  - Use `large` for accuracy when acceptable
- Warm up models on server start
- Example streaming:
  ```python
  @app.websocket("/ws/transcribe")
  async def transcribe_stream(websocket: WebSocket):
      await websocket.accept()
      async for audio_chunk in websocket.iter_bytes():
          partial_transcript = await whisper.transcribe_chunk(audio_chunk)
          await websocket.send_json({"transcript": partial_transcript})
  ```

### 4.2 Audio Device Selection
- **Auto-detection**: Enumerate devices, prefer VB-Audio Cable
  ```python
  import sounddevice as sd
  
  def auto_select_device():
      devices = sd.query_devices()
      vb_cable = next((d for d in devices if 'VB-Audio' in d['name']), None)
      return vb_cable['index'] if vb_cable else sd.default.device
  ```
- **Manual Override**: Allow user selection in settings
- **Test Audio**: Provide button to verify device works
- **Error Handling**: Graceful fallback if device unavailable

### 4.3 Speech-to-Text
- Use OpenAI Whisper for high accuracy
- Enable language auto-detection
- Return confidence scores
- Handle silence/noise (VAD - Voice Activity Detection)
- Example:
  ```python
  import whisper
  
  model = whisper.load_model("large")
  
  def transcribe_audio(audio_path: str):
      result = model.transcribe(
          audio_path,
          language="en",  # or None for auto-detect
          task="transcribe",
          fp16=False  # Use fp16=True on GPU
      )
      return {
          "text": result["text"],
          "language": result["language"],
          "segments": result["segments"]
      }
  ```

---

## 5. Session Tracking

### 5.1 Persistent Sessions
- Generate unique session IDs (UUID v4)
- Save to Firebase Firestore in real-time
- Auto-save every 30 seconds or after each Q&A
- Implement optimistic locking for concurrent updates
- Example:
  ```python
  import uuid
  from datetime import datetime
  
  session_id = str(uuid.uuid4())
  session_data = {
      "id": session_id,
      "user_id": user_id,
      "created_at": datetime.utcnow(),
      "questions": [],
      "status": "active"
  }
  db.collection('sessions').document(session_id).set(session_data)
  ```

### 5.2 Exporting Data
- **JSON Export**: Raw data for developers
  ```python
  import json
  
  def export_to_json(session_id: str):
      session = db.collection('sessions').document(session_id).get()
      return json.dumps(session.to_dict(), indent=2)
  ```
- **PDF Export**: Formatted for sharing
  ```python
  from reportlab.lib.pagesizes import letter
  from reportlab.pdfgen import canvas
  
  def export_to_pdf(session_id: str):
      session = get_session(session_id)
      pdf = canvas.Canvas(f"session_{session_id}.pdf", pagesize=letter)
      pdf.drawString(100, 750, f"Interview Session: {session['created_at']}")
      # Add questions/answers
      pdf.save()
  ```

### 5.3 History
- List view with filters (date range, job role)
- Search by keywords
- Pagination (20 per page)
- Sort by date, duration, rating

---

## 6. LLM Integration (Groq + Ollama)

### 6.1 Tailored Responses
- Use STAR method prompts
- Incorporate user profile (experience, skills)
- Reference job description
- Example prompt template:
  ```python
  PROMPT_TEMPLATE = """
  You are interviewing for a {job_role} position.
  
  Candidate Profile:
  - Experience: {years_experience} years
  - Skills: {skills}
  
  Job Description:
  {job_description}
  
  Question: {question}
  
  Provide a STAR-method answer (Situation, Task, Action, Result).
  """
  
  prompt = PROMPT_TEMPLATE.format(
      job_role="Senior Software Engineer",
      years_experience=5,
      skills="Python, React, AWS",
      job_description=jd_text,
      question=interview_question
  )
  ```

### 6.2 Contextualization
- Maintain conversation history (last 5 Q&A pairs)
- Use sliding window for long conversations
- Store context in session state
- Example:
  ```python
  context = []
  for qa in session['questions'][-5:]:
      context.append(f"Q: {qa['question']}\nA: {qa['answer']}")
  
  full_prompt = "\n\n".join(context) + f"\n\nQ: {new_question}\nA:"
  ```

### 6.3 Data Privacy
- Don't retain data after session unless user opts in
- Anonymize before analytics
- Comply with GDPR/CCPA
- Allow data deletion requests

---

## 7. Performance Metrics

### 7.1 Track Response Time
- Instrument all endpoints with timing
- Use middleware for automatic tracking
  ```python
  import time
  
  @app.middleware("http")
  async def track_response_time(request: Request, call_next):
      start_time = time.time()
      response = await call_next(request)
      duration = time.time() - start_time
      response.headers["X-Response-Time"] = str(duration)
      logger.info(f"{request.url.path} took {duration:.3f}s")
      return response
  ```
- Alert if p95 > 100ms

### 7.2 Monitor Performance
- **Logging**: Structured JSON logs
  ```python
  import logging
  import json
  
  logger = logging.getLogger(__name__)
  
  def log_event(event_type, data):
      logger.info(json.dumps({
          "event": event_type,
          "timestamp": datetime.utcnow().isoformat(),
          "data": data
      }))
  ```
- **Prometheus Metrics**:
  ```python
  from prometheus_client import Counter, Histogram
  
  request_count = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
  request_duration = Histogram('http_request_duration_seconds', 'HTTP Request Duration')
  
  @app.get("/api/endpoint")
  @request_duration.time()
  async def endpoint():
      request_count.labels(method='GET', endpoint='/api/endpoint').inc()
      return {"status": "ok"}
  ```
- **Grafana Dashboards**: Visualize metrics

---

## 8. Additional Features

### 8.1 Multilingual
- Use Whisper's language detection
- Support 10+ languages
- UI i18n with next-intl
- Example:
  ```typescript
  import { useTranslations } from 'next-intl';
  
  export default function Component() {
    const t = useTranslations('Interview');
    return <h1>{t('title')}</h1>;
  }
  ```

### 8.2 Voice Cloning
- Integrate ElevenLabs or Coqui TTS
- Allow custom voice profiles
- Stream audio response in real-time
- Example:
  ```python
  from elevenlabs import generate, stream
  
  def text_to_speech(text: str, voice_id: str):
      audio_stream = generate(
          text=text,
          voice=voice_id,
          model="eleven_monolingual_v1",
          stream=True
      )
      return stream(audio_stream)
  ```

### 8.3 WebSocket
- Use for all real-time features
- Implement reconnection logic
- Send heartbeat every 30s
- Close stale connections (5min timeout)

---

## 9. Deployment Guidelines

### 9.1 Cloud Resources
- **Frontend**: Vercel (free tier)
  - Automatic HTTPS
  - Edge functions for API routes
  - Preview deployments for PRs
- **Backend**: Render or Railway (free tier)
  - Dockerfile deployment
  - Auto-deploy from GitHub
  - Environment variables management
- **Database**: Firebase (Spark plan - free)
  - 1GB storage
  - 50K reads/day
  - 20K writes/day
- **LLM**: Google Cloud Vertex AI (pay-as-you-go)
  - $0.001 per 1K tokens
  - Groq for speed
  - Ollama local for development

### 9.2 Frontend Hosting
- Use `pnpm build` for optimized builds
- Enable compression (gzip/brotli)
- Set up custom domain
- Configure CDN caching
  ```javascript
  // next.config.js
  module.exports = {
    compress: true,
    images: {
      formats: ['image/webp'],
    },
  };
  ```

### 9.3 Scalability
- Horizontal scaling: Multiple FastAPI instances
- Load balancer: Nginx or cloud LB
- Database connection pooling
- Redis for session storage/caching
- CDN for static assets
- Example Docker setup:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

---

## 10. Security & Compliance

### 10.1 Regular Security Audits
- Run `npm audit` / `pip-audit` weekly
- Update dependencies monthly
- Use Dependabot for automated PRs
- OWASP Top 10 compliance

### 10.2 Privacy Standards
- **GDPR Compliance**:
  - Data portability (export feature)
  - Right to deletion (delete endpoint)
  - Consent management
- **HIPAA** (if handling health data):
  - Encrypted storage
  - Audit logs
  - Access controls

---

## 11. Code Review Checklist

Before submitting a PR, ensure:
- [ ] All tests pass (`pytest`, `npm test`)
- [ ] Code coverage >80%
- [ ] No linting errors (`flake8`, `eslint`)
- [ ] Documentation updated (README, API docs)
- [ ] Environment variables documented
- [ ] Performance tested (no regressions)
- [ ] Security scan passed
- [ ] Mobile responsive (tested on 3+ devices)

---

## 12. Git Workflow

- **Branch naming**: `feat/feature-name`, `fix/bug-name`, `docs/update-readme`
- **Commit messages**: Follow conventional commits
  - `feat: Add voice cloning support`
  - `fix: Resolve WebSocket disconnection issue`
  - `docs: Update API documentation`
- **PR template**: Include description, screenshots, testing steps
- **Code review**: Required for all changes
- **CI/CD**: Auto-deploy to staging on merge to `dev`, production on merge to `main`

---

## 13. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | <100ms | Prometheus |
| Frontend Load Time (p95) | <2s | Lighthouse |
| WebSocket Latency | <50ms | Custom instrumentation |
| Test Coverage | >80% | pytest-cov, Jest |
| Uptime | >99.9% | Sentry, StatusPage |
| Error Rate | <0.1% | Sentry |

---

## 14. Additional Notes

- Keep dependencies up-to-date (check monthly)
- Document all breaking changes in CHANGELOG.md
- Use semantic versioning (v1.0.0, v1.1.0, v2.0.0)
- Maintain backward compatibility for at least 2 major versions
- Write migration guides for major version updates

---

**Remember**: Code quality and user experience are paramount. When in doubt, prioritize simplicity, security, and performance.
