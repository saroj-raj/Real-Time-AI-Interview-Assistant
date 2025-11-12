# Complete Testing Guide

## Pre-Deployment Testing Checklist

### Phase 1: Environment Setup

- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` files configured (backend & frontend)
- [ ] Firebase project created
- [ ] Firebase service account JSON downloaded
- [ ] OpenAI API key obtained
- [ ] (Optional) Pinecone account created

### Phase 2: Backend Testing

#### 2.1 Server Startup
```bash
cd backend
python main.py
```

**Expected Output:**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Verify:**
- [ ] Server starts without errors
- [ ] Whisper model loads successfully
- [ ] Firebase connection established
- [ ] OpenAI client initialized

#### 2.2 Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

#### 2.3 WebSocket Connection Test

Open browser console at `http://localhost:3000`:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/interview/test-session');

ws.onopen = () => console.log('✅ Connected');
ws.onerror = (e) => console.error('❌ Error:', e);
ws.onclose = () => console.log('🔌 Disconnected');
ws.onmessage = (e) => console.log('📨 Message:', JSON.parse(e.data));
```

**Verify:**
- [ ] WebSocket connects successfully
- [ ] No errors in browser console
- [ ] No errors in backend logs

### Phase 3: Frontend Testing

#### 3.1 Development Server
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
✓ Ready in 2s
○ Local: http://localhost:3000
```

**Verify:**
- [ ] Server starts without errors
- [ ] No TypeScript errors
- [ ] Firebase config loaded

#### 3.2 Authentication Flow

**Test Login:**
1. Navigate to `http://localhost:3000/login`
2. Enter test email/password or use Google OAuth
3. Should redirect to dashboard

**Verify:**
- [ ] Login form renders
- [ ] Email/password login works
- [ ] Google OAuth works
- [ ] Redirects to dashboard after login
- [ ] User state persists on refresh

#### 3.3 Dashboard Testing

**Test Resume Upload:**
1. Click "Upload Resume"
2. Select PDF/DOCX/TXT file
3. Wait for upload

**Verify:**
- [ ] File upload dialog opens
- [ ] File uploads to Firebase Storage
- [ ] Resume appears in list
- [ ] Can delete resume

**Test Job Description:**
1. Click "Add Job Description"
2. Fill in company, role, description
3. Save

**Verify:**
- [ ] Form validation works
- [ ] JD saves to Firestore
- [ ] JD appears in list
- [ ] Can edit/delete JD

**Test Quick Start:**
1. Select resume and JD
2. Click "Quick Start Interview"
3. Should go to setup page

**Verify:**
- [ ] Can select resume
- [ ] Can select JD
- [ ] Navigates to setup

### Phase 4: Interview Setup Testing

**Test Setup Page:**
1. Company/role pre-filled from JD
2. Toggle "Follow-up Interview"
3. Click "Start Interview"

**Verify:**
- [ ] Form fields populated correctly
- [ ] Follow-up toggle works
- [ ] Creates session in Firestore
- [ ] Navigates to interview page
- [ ] Session ID in URL

### Phase 5: Live Interview Testing

#### 5.1 Audio Capture

**Test Microphone Access:**
1. Click "Start Listening"
2. Allow microphone permissions
3. Speak into microphone

**Verify:**
- [ ] Browser requests mic permission
- [ ] Permission granted successfully
- [ ] MediaRecorder starts
- [ ] Audio chunks generated
- [ ] Chunks sent to WebSocket
- [ ] Backend receives audio data

**Check Browser Console:**
```javascript
// Should see:
WebSocket connected
Sending audio chunk: ArrayBuffer(4096)
```

**Check Backend Logs:**
```
INFO:     WebSocket connection established: test-session
INFO:     Received audio chunk: 4096 bytes
```

#### 5.2 Transcription

**Test Speech Recognition:**
1. Start listening
2. Speak clearly: "Hello, can you hear me?"
3. Wait 3 seconds for transcription

**Verify:**
- [ ] Transcript appears in UI
- [ ] Text is accurate
- [ ] Speaker detection works (if enabled)
- [ ] Timestamp displayed correctly

**Backend Logs:**
```
INFO:     Transcribing audio buffer: 48000 samples
INFO:     Transcript: "Hello, can you hear me?"
```

#### 5.3 Question Detection

**Test Question Recognition:**
1. Ask: "Tell me about your experience with Python"
2. Wait for detection

**Verify:**
- [ ] Question highlighted in transcript
- [ ] Current question displayed in card
- [ ] "Generating answer..." appears

**Backend Logs:**
```
INFO:     Question detected: "Tell me about your experience with Python"
INFO:     Type: technical, Confidence: 0.85
```

#### 5.4 Answer Generation

**Test AI Answer:**
1. Wait for answer generation
2. Answer should appear in card

**Verify:**
- [ ] Answer generated within 2-3 seconds
- [ ] Answer is relevant to question
- [ ] Answer references resume/JD
- [ ] Confidence score displayed
- [ ] Context used shown

**Backend Logs:**
```
INFO:     Generating answer for question: qa-123456
INFO:     Using context: Resume (Experience), JD (Required Skills)
INFO:     Answer generated: 300 tokens, confidence: 0.87
```

#### 5.5 Answer Actions

**Test Copy Answer:**
1. Click "Copy" button
2. Paste in text editor

**Verify:**
- [ ] Answer copied to clipboard
- [ ] Paste shows correct text

**Test Regenerate Answer:**
1. Click "Regenerate" button
2. Wait for new answer

**Verify:**
- [ ] New answer different from original
- [ ] Still relevant to question
- [ ] Updates in UI

**Test Mark as Used:**
1. Click "Mark as Used" button
2. Check Firestore

**Verify:**
- [ ] Button shows checkmark
- [ ] Firestore `wasUsed` = true
- [ ] Tracked for self-learning

#### 5.6 Session Controls

**Test Pause:**
1. Click "Pause" button
2. Speak into microphone

**Verify:**
- [ ] Audio capture stops
- [ ] No new transcripts appear
- [ ] Timer pauses
- [ ] Can resume

**Test Stop:**
1. Click "Stop Interview"
2. Check session in Firestore

**Verify:**
- [ ] Session ends
- [ ] Final transcript saved
- [ ] All Q&A saved
- [ ] Duration recorded
- [ ] Status = "completed"

### Phase 6: Data Persistence Testing

#### 6.1 Firebase Firestore

**Check Collections:**
- [ ] `users/{userId}` exists
- [ ] `resumes/{resumeId}` exists
- [ ] `job_descriptions/{jdId}` exists
- [ ] `sessions/{sessionId}` exists
- [ ] `sessions/{sessionId}/transcripts` has documents
- [ ] `sessions/{sessionId}/questions_answers` has documents

**Verify Session Data:**
```json
{
  "userId": "abc123",
  "resumeId": "resume-1",
  "jobDescriptionId": "jd-1",
  "status": "completed",
  "startedAt": "2025-01-01T10:00:00Z",
  "endedAt": "2025-01-01T10:30:00Z",
  "duration": 1800,
  "isFollowUp": false
}
```

#### 6.2 Firebase Storage

**Check Files:**
- [ ] `resumes/{userId}/{resumeId}.pdf` uploaded
- [ ] (Future) `audio/{sessionId}/recording.webm` saved

### Phase 7: Follow-Up Interview Testing

**Test Follow-Up Context:**
1. Complete initial interview
2. Start new interview with same JD
3. Toggle "Follow-up Interview"
4. Ask similar question

**Verify:**
- [ ] Previous session detected
- [ ] Answer references previous interview
- [ ] Context includes prior Q&A
- [ ] `parentSessionId` set in Firestore

### Phase 8: Multi-User Testing

**Test User Isolation:**
1. Create User A account
2. Upload resume, add JD, start interview
3. Log out
4. Create User B account
5. Check dashboard

**Verify:**
- [ ] User B doesn't see User A's data
- [ ] Resumes isolated by userId
- [ ] Sessions isolated by userId
- [ ] JDs isolated by userId

### Phase 9: Error Handling

#### 9.1 Network Errors

**Test WebSocket Disconnect:**
1. Start interview
2. Stop backend server
3. Check frontend behavior

**Verify:**
- [ ] Shows disconnection message
- [ ] Attempts to reconnect
- [ ] Data saved before disconnect

**Test Resume Upload Failure:**
1. Disconnect internet
2. Try uploading resume

**Verify:**
- [ ] Shows error message
- [ ] Doesn't corrupt UI state

#### 9.2 Permission Errors

**Test Microphone Denied:**
1. Start interview
2. Deny mic permission

**Verify:**
- [ ] Shows helpful error message
- [ ] Doesn't crash app
- [ ] Can retry

#### 9.3 API Errors

**Test OpenAI Rate Limit:**
1. Generate many answers quickly
2. Hit rate limit

**Verify:**
- [ ] Shows error message
- [ ] Can retry
- [ ] Session not corrupted

### Phase 10: Performance Testing

**Test Long Sessions:**
1. Run interview for 30+ minutes
2. Ask 20+ questions

**Verify:**
- [ ] No memory leaks
- [ ] WebSocket stable
- [ ] Transcript loads quickly
- [ ] Firestore writes successful

**Test Large Resumes:**
1. Upload 10-page resume
2. Ask questions

**Verify:**
- [ ] Parsing completes
- [ ] Context extraction works
- [ ] Answer generation not too slow

### Phase 11: Cross-Browser Testing

**Browsers to Test:**
- [ ] Chrome (desktop)
- [ ] Firefox (desktop)
- [ ] Safari (desktop)
- [ ] Edge (desktop)
- [ ] Chrome (mobile)
- [ ] Safari (mobile iOS)

**Verify Each Browser:**
- [ ] MediaRecorder API works
- [ ] WebSocket connections work
- [ ] Firebase auth works
- [ ] UI renders correctly
- [ ] Audio capture functional

### Phase 12: Mobile Testing

**Test Responsive Design:**
- [ ] Login page mobile-friendly
- [ ] Dashboard usable on mobile
- [ ] Setup page fits screen
- [ ] Interview page readable
- [ ] Buttons large enough to tap

**Test Mobile Audio:**
- [ ] Mic permission works
- [ ] Audio capture on iOS
- [ ] Audio capture on Android
- [ ] WebSocket on mobile network

## Common Issues & Solutions

### Issue: Whisper Not Transcribing
**Solution:**
- Check audio format (should be 16kHz mono)
- Verify Whisper model loaded
- Check buffer size (min 3 seconds)
- Test with louder/clearer speech

### Issue: No Questions Detected
**Solution:**
- Check question patterns in `question_detector.py`
- Ask with clear question words (what, how, tell me)
- Verify transcript is accurate first
- Lower confidence threshold

### Issue: Poor Answer Quality
**Solution:**
- Check resume content (more detail = better answers)
- Verify JD has required skills
- Increase GPT-4 context window
- Adjust temperature (0.5-0.9)

### Issue: High Latency
**Solution:**
- Use smaller Whisper model (base instead of medium)
- Reduce buffer size to 2 seconds
- Use gpt-4-turbo instead of gpt-4
- Optimize resume context extraction

### Issue: Firebase Permission Denied
**Solution:**
- Check Firestore rules
- Verify user authenticated
- Check service account permissions
- Test with admin SDK

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] No console errors
- [ ] Firebase security rules configured
- [ ] Environment variables in production
- [ ] API keys secured (not in code)
- [ ] CORS configured for production domain
- [ ] Frontend built for production (`npm run build`)
- [ ] Backend deployed to cloud (Render/Railway)
- [ ] Database backups enabled
- [ ] Monitoring set up (logs, errors)
- [ ] Cost limits set (OpenAI, Firebase)

## Success Criteria

✅ **Ready for Deployment When:**
1. User can sign up and log in
2. User can upload resume and add JD
3. User can start interview session
4. Microphone captures audio
5. Audio transcribes accurately (>80% accuracy)
6. Questions detected (>70% accuracy)
7. Answers generated within 3 seconds
8. Answers are relevant and personalized
9. All data saves to Firebase
10. Sessions persist after refresh
11. Multi-user isolation works
12. No critical errors in 30-minute session
13. Works on Chrome, Firefox, Safari
14. Mobile responsive and functional

## Post-Deployment Monitoring

**Week 1:**
- Monitor error rates
- Track answer generation latency
- Check OpenAI costs
- Review user feedback
- Fix critical bugs

**Week 2:**
- Analyze answer quality
- Improve question detection
- Optimize performance
- Add missing features

**Ongoing:**
- Train self-learning model
- Improve answer personalization
- Add new question types
- Optimize costs
