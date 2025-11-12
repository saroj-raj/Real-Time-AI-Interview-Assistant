import asyncio
import json
import logging
from typing import Dict, Optional
import numpy as np
import soundfile as sf
import io

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handles audio stream processing and buffering"""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.audio_buffer = []
        
    def process_chunk(self, audio_bytes: bytes) -> np.ndarray:
        """Convert audio bytes to numpy array"""
        try:
            audio_data, _ = sf.read(io.BytesIO(audio_bytes))
            return audio_data
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            return np.array([])
    
    def add_to_buffer(self, audio_data: np.ndarray):
        """Add audio data to buffer"""
        self.audio_buffer.append(audio_data)
    
    def get_buffer(self, clear: bool = True) -> np.ndarray:
        """Get buffered audio and optionally clear"""
        if not self.audio_buffer:
            return np.array([])
        
        combined = np.concatenate(self.audio_buffer)
        if clear:
            self.audio_buffer = []
        return combined
    
    def save_audio(self, filepath: str, audio_data: np.ndarray):
        """Save audio to file"""
        sf.write(filepath, audio_data, self.sample_rate)
