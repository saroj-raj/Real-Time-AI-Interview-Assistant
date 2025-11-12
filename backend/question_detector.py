import logging
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class QuestionDetector:
    """Detects when a question is being asked using pattern matching and heuristics"""
    
    def __init__(self):
        # Common question patterns
        self.question_patterns = [
            r'\b(what|when|where|who|why|how|which)\b',
            r'\b(tell me|describe|explain|discuss|talk about)\b',
            r'\b(can you|could you|would you|will you)\b',
            r'\b(do you|did you|have you|are you|were you)\b',
            r'\?$',  # Ends with question mark
        ]
        
        # Compile patterns
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.question_patterns
        ]
    
    def is_question(self, text: str) -> Dict[str, Any]:
        """
        Determine if text is a question
        
        Returns:
            dict with 'is_question' (bool), 'confidence' (float), 'type' (str)
        """
        if not text or len(text.strip()) < 5:
            return {
                "is_question": False,
                "confidence": 0.0,
                "type": None
            }
        
        text = text.strip()
        matches = 0
        
        # Check patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                matches += 1
        
        # Calculate confidence based on matches
        confidence = min(matches / 2.0, 1.0)  # 2+ matches = high confidence
        
        # Determine question type
        question_type = self._determine_type(text)
        
        is_question = matches >= 1 or text.endswith('?')
        
        return {
            "is_question": is_question,
            "confidence": confidence if is_question else 0.0,
            "type": question_type if is_question else None
        }
    
    def _determine_type(self, text: str) -> str:
        """Determine question type (technical, behavioral, situational)"""
        text_lower = text.lower()
        
        # Behavioral indicators
        behavioral_keywords = [
            'tell me about a time',
            'describe a situation',
            'give me an example',
            'experience with',
            'challenge you faced',
            'conflict',
            'team',
            'leadership'
        ]
        
        # Technical indicators
        technical_keywords = [
            'how does',
            'explain',
            'implement',
            'algorithm',
            'system design',
            'architecture',
            'code',
            'database',
            'api',
            'performance'
        ]
        
        for keyword in behavioral_keywords:
            if keyword in text_lower:
                return 'behavioral'
        
        for keyword in technical_keywords:
            if keyword in text_lower:
                return 'technical'
        
        return 'general'
    
    def extract_questions(self, segments: List[Dict[str, str]]) -> List[Dict]:
        """
        Extract questions from transcript segments
        
        Args:
            segments: List of transcript segments with 'speaker' and 'text'
        
        Returns:
            List of detected questions with metadata
        """
        questions = []
        
        for i, segment in enumerate(segments):
            if segment.get('speaker') == 'recruiter':
                result = self.is_question(segment.get('text', ''))
                
                if result['is_question']:
                    questions.append({
                        'text': segment['text'],
                        'timestamp': segment.get('timestamp', 0),
                        'confidence': result['confidence'],
                        'type': result['type'],
                        'segment_index': i
                    })
        
        return questions
