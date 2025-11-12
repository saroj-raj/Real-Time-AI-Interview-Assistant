import whisper
import logging
from typing import Optional, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class TranscriptionService:
    """Handles real-time transcription using Whisper"""
    
    def __init__(self, model_name: str = "base"):
        logger.info(f"Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)
        self.sample_rate = 16000
    
    def transcribe_audio(
        self, 
        audio_data: np.ndarray, 
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Transcribe audio data
        
        Returns:
            dict with 'text', 'language', 'confidence'
        """
        try:
            if len(audio_data) == 0:
                return {"text": "", "language": language, "confidence": 0.0}
            
            # Ensure audio is float32 and normalized
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Transcribe
            result = self.model.transcribe(
                audio_data,
                language=language,
                fp16=False,
                verbose=False
            )
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", language),
                "confidence": self._calculate_confidence(result)
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {"text": "", "language": language, "confidence": 0.0}
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate average confidence from segments"""
        if "segments" not in result or not result["segments"]:
            return 0.0
        
        confidences = []
        for segment in result["segments"]:
            if "no_speech_prob" in segment:
                # Convert no_speech_prob to confidence
                confidences.append(1.0 - segment["no_speech_prob"])
        
        return sum(confidences) / len(confidences) if confidences else 0.5
