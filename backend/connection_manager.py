import asyncio
import logging
from typing import Dict, Set
from fastapi import WebSocket
import json

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time communication"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_data: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.session_data[session_id] = {
            "audio_buffer": [],
            "transcript": [],
            "questions": []
        }
        logger.info(f"Client connected for session: {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.session_data:
            del self.session_data[session_id]
        logger.info(f"Client disconnected for session: {session_id}")
    
    async def send_message(self, session_id: str, message: Dict):
        """Send message to specific session"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {session_id}: {e}")
    
    async def send_transcript(
        self, 
        session_id: str, 
        text: str, 
        speaker: str, 
        is_final: bool = True
    ):
        """Send transcript update"""
        await self.send_message(session_id, {
            "type": "transcript",
            "data": {
                "text": text,
                "speaker": speaker,
                "isFinal": is_final
            },
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def send_question_detected(
        self,
        session_id: str,
        question: str,
        confidence: float
    ):
        """Send question detection notification"""
        await self.send_message(session_id, {
            "type": "question_detected",
            "data": {
                "question": question,
                "confidence": confidence
            },
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def send_answer(
        self,
        session_id: str,
        question_id: str,
        answer: str,
        confidence: float,
        context_used: Dict
    ):
        """Send generated answer"""
        await self.send_message(session_id, {
            "type": "answer_generated",
            "data": {
                "questionId": question_id,
                "answer": answer,
                "confidence": confidence,
                "contextUsed": context_used
            },
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def send_error(self, session_id: str, error: str):
        """Send error message"""
        await self.send_message(session_id, {
            "type": "error",
            "data": {"message": error},
            "timestamp": asyncio.get_event_loop().time()
        })
    
    def add_to_buffer(self, session_id: str, audio_chunk: bytes):
        """Add audio chunk to session buffer"""
        if session_id in self.session_data:
            self.session_data[session_id]["audio_buffer"].append(audio_chunk)
    
    def get_buffer(self, session_id: str, clear: bool = False) -> list:
        """Get audio buffer for session"""
        if session_id in self.session_data:
            buffer = self.session_data[session_id]["audio_buffer"]
            if clear:
                self.session_data[session_id]["audio_buffer"] = []
            return buffer
        return []
