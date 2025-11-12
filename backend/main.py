from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv
import asyncio

# Import custom modules
from connection_manager import ConnectionManager
from transcription_service import TranscriptionService
from question_detector import QuestionDetector
from answer_generator import AnswerGenerator
from firebase_service import FirebaseService
from audio_processor import AudioProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="AI Interview Assistant API", version="1.0.0")

# Initialize services
connection_manager = ConnectionManager()
transcription_service = TranscriptionService(model_name=os.getenv("WHISPER_MODEL", "base"))
question_detector = QuestionDetector()
answer_generator = AnswerGenerator()
firebase_service = FirebaseService()
audio_processor = AudioProcessor()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class TranscriptRequest(BaseModel):
    audio_url: str
    session_id: str

class QuestionDetectedResponse(BaseModel):
    question: str
    timestamp: float
    confidence: float

class AnswerGenerationRequest(BaseModel):
    question: str
    session_id: str
    resume_id: str
    jd_id: str

class AnswerGenerationResponse(BaseModel):
    answer: str
    confidence: float
    context_used: dict

# Health Check
@app.get("/")
async def root():
    return {
        "message": "AI Interview Assistant API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# WebSocket for real-time transcription
@app.websocket("/ws/interview/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await connection_manager.connect(websocket, session_id)
    logger.info(f"WebSocket connection established for session: {session_id}")
    
    # Get session data from Firebase
    session_data = firebase_service.get_session(session_id)
    if not session_data:
        await connection_manager.send_error(session_id, "Session not found")
        connection_manager.disconnect(session_id)
        return
    
    # Get resume and JD data
    resume_data = firebase_service.get_resume(session_data['resumeId'])
    jd_data = firebase_service.get_job_description(session_data['jobDescriptionId'])
    
    if not resume_data or not jd_data:
        await connection_manager.send_error(session_id, "Resume or JD not found")
        connection_manager.disconnect(session_id)
        return
    
    # Get previous sessions for context (if follow-up)
    previous_qa = []
    if session_data.get('isFollowUp'):
        prev_sessions = firebase_service.get_previous_sessions(
            session_data['userId'],
            session_data['companyName']
        )
        # Get Q&A from previous sessions
        # TODO: Implement fetching previous Q&A
    
    audio_buffer = []
    
    try:
        while True:
            # Receive audio chunks from client
            data = await websocket.receive_bytes()
            audio_buffer.append(data)
            
            # Process every 3 seconds of audio
            if len(audio_buffer) >= 30:  # ~3 seconds at 10 chunks/sec
                # Combine audio chunks
                combined_audio = b''.join(audio_buffer)
                audio_buffer = []
                
                # Process audio
                audio_array = audio_processor.process_chunk(combined_audio)
                
                if len(audio_array) > 0:
                    # Transcribe
                    transcription_result = transcription_service.transcribe_audio(audio_array)
                    transcript_text = transcription_result['text']
                    
                    if transcript_text:
                        # For now, assume all audio is from recruiter
                        # TODO: Implement speaker diarization
                        speaker = 'recruiter'
                        
                        # Send transcript to client
                        await connection_manager.send_transcript(
                            session_id,
                            transcript_text,
                            speaker,
                            is_final=True
                        )
                        
                        # Save transcript to Firebase
                        firebase_service.save_transcript_segment(session_id, {
                            'speaker': speaker,
                            'text': transcript_text,
                            'timestamp': asyncio.get_event_loop().time(),
                            'isFinal': True
                        })
                        
                        # Check if it's a question
                        question_result = question_detector.is_question(transcript_text)
                        
                        if question_result['is_question']:
                            # Notify client that question was detected
                            await connection_manager.send_question_detected(
                                session_id,
                                transcript_text,
                                question_result['confidence']
                            )
                            
                            # Generate answer
                            answer_result = answer_generator.generate_answer(
                                question=transcript_text,
                                resume_data=resume_data,
                                jd_data=jd_data,
                                question_type=question_result['type'],
                                previous_context=previous_qa
                            )
                            
                            # Send answer to client
                            question_id = f"{session_id}_{int(asyncio.get_event_loop().time())}"
                            await connection_manager.send_answer(
                                session_id,
                                question_id,
                                answer_result['answer'],
                                answer_result['confidence'],
                                answer_result['context_used']
                            )
                            
                            # Save Q&A to Firebase
                            firebase_service.save_question_answer(session_id, {
                                'question': transcript_text,
                                'questionTimestamp': asyncio.get_event_loop().time(),
                                'suggestedAnswer': answer_result['answer'],
                                'confidence': answer_result['confidence'],
                                'contextUsed': answer_result['context_used'],
                                'wasUsed': False
                            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session: {session_id}")
        connection_manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        await connection_manager.send_error(session_id, str(e))
        connection_manager.disconnect(session_id)

# Resume Upload & Parsing
@app.post("/api/v1/resume/upload")
async def upload_resume(file: UploadFile = File(...), user_id: str = ""):
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # TODO: Upload to Firebase Storage
    # TODO: Parse resume with PyPDF2/python-docx
    # TODO: Extract skills, experience, projects
    # TODO: Store in Firestore
    
    return {
        "message": "Resume uploaded successfully",
        "file_name": file.filename,
        "user_id": user_id
    }

# Answer Generation (RAG)
@app.post("/api/v1/answer/generate", response_model=AnswerGenerationResponse)
async def generate_answer(request: AnswerGenerationRequest):
    # TODO: Retrieve resume from Firestore
    # TODO: Retrieve JD from Firestore
    # TODO: Semantic search in vector DB for relevant context
    # TODO: Generate answer using LLM with context
    
    return AnswerGenerationResponse(
        answer="Simulated personalized answer based on your resume and JD...",
        confidence=0.92,
        context_used={
            "resume_section": "Experience > Project ABC",
            "jd_section": "Required Skills > Python, AI"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
