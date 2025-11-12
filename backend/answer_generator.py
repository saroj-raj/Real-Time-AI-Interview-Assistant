import logging
from typing import Dict, List, Optional, Any
import os
import requests
import json
from groq import Groq

logger = logging.getLogger(__name__)

class AnswerGenerator:
    """Generates personalized interview answers using Groq/Ollama + RAG context"""
    
    def __init__(self, api_key: Optional[str] = None, use_ollama: bool = False):
        """
        Initialize Answer Generator with Groq or Ollama
        
        Args:
            api_key: Groq API key (free from console.groq.com)
            use_ollama: If True, use local Ollama instead of Groq
        """
        self.use_ollama = use_ollama
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.groq_client = None
        
        if not use_ollama:
            # Use Groq API (free, fast)
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                logger.warning("Groq API key not found, falling back to Ollama")
                self.use_ollama = True
            else:
                try:
                    self.groq_client = Groq(api_key=self.api_key)
                    self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                    logger.info(f"Using Groq API with model: {self.model}")
                except Exception as e:
                    logger.warning(f"Failed to initialize Groq client: {e}. Falling back to Ollama")
                    self.use_ollama = True
        
        if self.use_ollama:
            # Use local Ollama
            self.model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
            logger.info(f"Using Ollama with model: {self.model}")
        
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "300"))
    
    def generate_answer(
        self,
        question: str,
        resume_data: Dict,
        jd_data: Dict,
        question_type: str = "general",
        previous_context: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized answer based on question and context
        
        Args:
            question: The interview question
            resume_data: Parsed resume data
            jd_data: Job description data
            question_type: 'technical', 'behavioral', or 'general'
            previous_context: Previous Q&A from follow-up interviews
            
        Returns:
            Dict with answer, confidence, and context_used
        """
        try:
            # Extract relevant context from resume
            resume_context = self._extract_resume_context(resume_data, question)
            
            # Extract relevant context from job description
            jd_context = self._extract_jd_context(jd_data, question)
            
            # Build previous Q&A context for follow-up interviews
            previous_qa_context = ""
            if previous_context and len(previous_context) > 0:
                previous_qa_context = "\n\nPREVIOUS INTERVIEW CONTEXT:\n"
                for qa in previous_context[-3:]:  # Last 3 Q&As
                    previous_qa_context += f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}\n\n"
            
            # Build system prompt based on question type
            system_prompt = self._build_system_prompt(question_type)
            
            # Build user prompt with context
            user_prompt = f"""
QUESTION: {question}

YOUR BACKGROUND:
{resume_context}

JOB REQUIREMENTS:
{jd_context}
{previous_qa_context}

Provide a concise, personalized answer (2-3 sentences max) that:
1. Directly addresses the question
2. References YOUR specific experience from the background
3. Aligns with the job requirements
4. Sounds natural and confident

Answer:"""

            # Call LLM (Groq or Ollama)
            answer_text = self._call_llm(system_prompt, user_prompt)
            
            # Calculate confidence based on context match
            confidence = self._calculate_confidence(
                question, answer_text, resume_context, jd_context
            )
            
            return {
                "answer": answer_text.strip(),
                "confidence": confidence,
                "context_used": {
                    "resume_section": self._get_context_sections(resume_context),
                    "jd_section": self._get_context_sections(jd_context)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "answer": "I have relevant experience with this. Let me elaborate...",
                "confidence": 0.5,
                "context_used": {}
            }
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call Groq API or Ollama to generate answer"""
        try:
            if self.use_ollama:
                # Call local Ollama
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{user_prompt}",
                        "stream": False,
                        "options": {
                            "temperature": self.temperature,
                            "num_predict": self.max_tokens
                        }
                    },
                    timeout=30
                )
                response.raise_for_status()
                return response.json().get("response", "")
            
            else:
                # Call Groq API using SDK
                if not self.groq_client:
                    raise ValueError("Groq client not initialized")
                    
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return chat_completion.choices[0].message.content or ""
                
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            if not self.use_ollama:
                # Try falling back to Ollama
                logger.info("Falling back to Ollama...")
                self.use_ollama = True
                return self._call_llm(system_prompt, user_prompt)
            raise
    
    def _build_system_prompt(self, question_type: str) -> str:
        """Build system prompt based on question type"""
        base_prompt = "You are an interview candidate responding to questions. "
        
        if question_type == "behavioral":
            return base_prompt + """Use the STAR format (Situation, Task, Action, Result) 
to structure your answer. Be specific and concise."""
        
        elif question_type == "technical":
            return base_prompt + """Demonstrate technical depth with specific examples from your experience. 
Mention technologies, tools, and measurable outcomes."""
        
        else:  # general
            return base_prompt + """Answer clearly and confidently, backing up claims with 
specific examples from your experience."""
    
    def _extract_resume_context(self, resume_data: Dict, question: str) -> str:
        """Extract relevant sections from resume based on question"""
        context_parts = []
        
        # Extract skills
        skills = resume_data.get("parsedData", {}).get("skills", [])
        if skills:
            context_parts.append(f"Skills: {', '.join(skills[:10])}")
        
        # Extract experience
        experiences = resume_data.get("parsedData", {}).get("experience", [])
        if experiences:
            for exp in experiences[:2]:  # Top 2 experiences
                context_parts.append(
                    f"{exp.get('role', '')} at {exp.get('company', '')} ({exp.get('duration', '')}): "
                    f"{exp.get('description', '')[:200]}"
                )
        
        # Extract projects
        projects = resume_data.get("parsedData", {}).get("projects", [])
        if projects:
            for proj in projects[:2]:  # Top 2 projects
                context_parts.append(
                    f"Project: {proj.get('name', '')} - {proj.get('description', '')[:150]}"
                )
        
        return "\n".join(context_parts) if context_parts else "No resume context available"
    
    def _extract_jd_context(self, jd_data: Dict, question: str) -> str:
        """Extract relevant sections from job description"""
        context_parts = []
        
        # Required skills
        required_skills = jd_data.get("requiredSkills", [])
        if required_skills:
            context_parts.append(f"Required Skills: {', '.join(required_skills[:8])}")
        
        # Responsibilities
        responsibilities = jd_data.get("responsibilities", [])
        if responsibilities:
            context_parts.append(f"Key Responsibilities: {', '.join(responsibilities[:3])}")
        
        # Company and role
        company = jd_data.get("companyName", "")
        role = jd_data.get("roleName", "")
        if company and role:
            context_parts.append(f"Role: {role} at {company}")
        
        return "\n".join(context_parts) if context_parts else "No job description context available"
    
    def _calculate_confidence(
        self, question: str, answer: str, resume_ctx: str, jd_ctx: str
    ) -> float:
        """Calculate confidence score based on context overlap"""
        # Simple keyword overlap score
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        context_words = set((resume_ctx + " " + jd_ctx).lower().split())
        
        # Check overlap between answer and context
        overlap = len(answer_words & context_words)
        total = len(answer_words)
        
        if total == 0:
            return 0.5
        
        confidence = min(0.95, max(0.5, overlap / total))
        return round(confidence, 2)
    
    def _get_context_sections(self, context: str) -> str:
        """Extract section names from context"""
        lines = context.split("\n")
        sections = []
        for line in lines:
            if ":" in line:
                section = line.split(":")[0].strip()
                if section and len(section) < 50:
                    sections.append(section)
        return ", ".join(sections[:3]) if sections else "General context"
