import logging
from typing import Dict, List, Optional
import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

logger = logging.getLogger(__name__)

class FirebaseService:
    """Handles Firebase Firestore and Storage operations"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.enabled = False
        self.db = None
        self.bucket = None
        
        try:
            if not firebase_admin._apps:
                cred_path = credentials_path or os.getenv("FIREBASE_CREDENTIALS_PATH")
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred, {
                        'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")
                    })
                    self.db = firestore.client()
                    self.bucket = storage.bucket()
                    self.enabled = True
                    logger.info("Firebase initialized successfully")
                else:
                    logger.warning("Firebase credentials not found. Running in mock mode.")
            else:
                self.db = firestore.client()
                self.bucket = storage.bucket()
                self.enabled = True
        except Exception as e:
            logger.warning(f"Firebase initialization failed: {e}. Running in mock mode.")
    
    def get_resume(self, resume_id: str) -> Optional[Dict]:
        """Get resume data from Firestore"""
        if not self.enabled or not self.db:
            return {"parsedData": {"skills": [], "experience": [], "projects": []}}
        try:
            doc = self.db.collection('resumes').document(resume_id).get()
            if doc.exists:
                return {**doc.to_dict(), 'id': doc.id}
            return None
        except Exception as e:
            logger.error(f"Error fetching resume: {e}")
            return None
    
    def get_job_description(self, jd_id: str) -> Optional[Dict]:
        """Get job description from Firestore"""
        if not self.enabled or not self.db:
            return {"requiredSkills": [], "responsibilities": [], "companyName": "Test Company", "roleName": "Test Role"}
        try:
            doc = self.db.collection('jobDescriptions').document(jd_id).get()
            if doc.exists:
                return {**doc.to_dict(), 'id': doc.id}
            return None
        except Exception as e:
            logger.error(f"Error fetching JD: {e}")
            return None
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get interview session data"""
        if not self.enabled or not self.db:
            return {"userId": "test", "resumeId": "test", "jdId": "test"}
        try:
            doc = self.db.collection('interviewSessions').document(session_id).get()
            if doc.exists:
                return {**doc.to_dict(), 'id': doc.id}
            return None
        except Exception as e:
            logger.error(f"Error fetching session: {e}")
            return None
    
    def get_previous_sessions(
        self, 
        user_id: str, 
        company_name: str, 
        limit: int = 3
    ) -> List[Dict]:
        """Get previous interview sessions for context (follow-up interviews)"""
        if not self.enabled or not self.db:
            return []
        try:
            sessions = (
                self.db.collection('interviewSessions')
                .where('userId', '==', user_id)
                .where('companyName', '==', company_name)
                .where('status', '==', 'completed')
                .order_by('createdAt', direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream()
            )
            return [{'id': doc.id, **doc.to_dict()} for doc in sessions]
        except Exception as e:
            logger.error(f"Error fetching previous sessions: {e}")
            return []
    
    def save_transcript_segment(self, session_id: str, segment: Dict):
        """Save transcript segment to Firestore"""
        if not self.enabled or not self.db:
            logger.info(f"Mock: Would save transcript segment for session {session_id}")
            return
        try:
            self.db.collection('transcriptSegments').add({
                **segment,
                'sessionId': session_id
            })
        except Exception as e:
            logger.error(f"Error saving transcript: {e}")
    
    def save_question_answer(self, session_id: str, qa: Dict):
        """Save question-answer pair to Firestore"""
        if not self.enabled or not self.db:
            logger.info(f"Mock: Would save Q&A for session {session_id}")
            return
        try:
            self.db.collection('questionsAnswers').add({
                **qa,
                'sessionId': session_id
            })
        except Exception as e:
            logger.error(f"Error saving Q&A: {e}")
    
    def update_session(self, session_id: str, updates: Dict):
        """Update session data"""
        if not self.enabled or not self.db:
            logger.info(f"Mock: Would update session {session_id}")
            return
        try:
            self.db.collection('interviewSessions').document(session_id).update(updates)
        except Exception as e:
            logger.error(f"Error updating session: {e}")
