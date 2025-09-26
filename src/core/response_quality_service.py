"""
Response Quality Control Service
Implements real-time validation, hallucination detection, and quality scoring
"""
import re
import json
import time
import threading
from typing import Dict, List, Optional, Tuple, Generator
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    STRICT = "strict"
    MODERATE = "moderate"
    PERMISSIVE = "permissive"

@dataclass
class QualityMetrics:
    """Quality metrics for interview responses"""
    confidence_score: float
    specificity_score: float
    relevance_score: float
    authenticity_score: float
    overall_score: float
    issues: List[str]
    suggestions: List[str]

class TechnicalFactChecker:
    """Validates technical accuracy in responses"""
    
    def __init__(self):
        # Known technology combinations and their validity
        self.valid_tech_combinations = {
            "langchain": ["openai", "pinecone", "weaviate", "chromadb", "faiss"],
            "langgraph": ["langchain", "openai", "anthropic"],
            "ragas": ["langchain", "openai", "huggingface"],
            "crewai": ["langchain", "openai"],
            "docker": ["kubernetes", "aws", "azure", "gcp"],
            "kubernetes": ["docker", "prometheus", "grafana"]
        }
        
        # Common technical inaccuracies to flag
        self.suspicious_claims = [
            r"reduced.*100%",  # 100% reductions are usually impossible
            r"achieved.*perfect.*accuracy",  # Perfect accuracy claims
            r"zero.*latency",  # Zero latency claims
            r"infinite.*scalability",  # Infinite scalability claims
            r"eliminated.*all.*errors"  # Error elimination claims
        ]
        
        # Valid API patterns for different frameworks
        self.valid_api_patterns = {
            "langchain": [
                r"from langchain import",
                r"LLMChain\(",
                r"ConversationChain\(",
                r"PromptTemplate\("
            ],
            "openai": [
                r"openai\.ChatCompletion\.create",
                r"openai\.Completion\.create",
                r"client\.chat\.completions\.create"
            ]
        }
    
    def validate_technical_content(self, response: str) -> Tuple[bool, List[str]]:
        """Validate technical accuracy of response content"""
        issues = []
        
        # Check for suspicious technical claims
        for pattern in self.suspicious_claims:
            if re.search(pattern, response, re.IGNORECASE):
                issues.append(f"Suspicious claim detected: {pattern}")
        
        # Validate code examples if present
        code_blocks = self._extract_code_blocks(response)
        for code_block in code_blocks:
            code_issues = self._validate_code_block(code_block)
            issues.extend(code_issues)
        
        # Check technology combination validity
        tech_issues = self._validate_technology_combinations(response)
        issues.extend(tech_issues)
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def _extract_code_blocks(self, response: str) -> List[str]:
        """Extract code blocks from response"""
        code_pattern = r'```(?:python|javascript|bash)?\n(.*?)```'
        return re.findall(code_pattern, response, re.DOTALL)
    
    def _validate_code_block(self, code: str) -> List[str]:
        """Validate individual code block for accuracy"""
        issues = []
        
        # Check for common fabricated patterns
        fabricated_patterns = [
            r"# Simplified example",
            r"# Example implementation",
            r"# This is just an example",
            r"example_.*=",  # Variables named example_*
        ]
        
        for pattern in fabricated_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append("Code appears to be fabricated example rather than actual implementation")
                break
        
        # Validate API usage
        for framework, patterns in self.valid_api_patterns.items():
            if framework in code.lower():
                valid_usage = any(re.search(pattern, code) for pattern in patterns)
                if not valid_usage:
                    issues.append(f"Invalid {framework} API usage detected")
        
        return issues
    
    def _validate_technology_combinations(self, response: str) -> List[str]:
        """Check if mentioned technologies are commonly used together"""
        issues = []
        response_lower = response.lower()
        
        mentioned_techs = []
        for tech in self.valid_tech_combinations.keys():
            if tech in response_lower:
                mentioned_techs.append(tech)
        
        # Check for unusual combinations
        for tech in mentioned_techs:
            compatible_techs = self.valid_tech_combinations.get(tech, [])
            other_mentioned = [t for t in mentioned_techs if t != tech]
            
            for other_tech in other_mentioned:
                if other_tech not in compatible_techs and tech not in self.valid_tech_combinations.get(other_tech, []):
                    issues.append(f"Unusual technology combination: {tech} with {other_tech}")
        
        return issues

class SpecificityAnalyzer:
    """Analyzes response specificity and concreteness"""
    
    def __init__(self):
        self.vague_phrases = [
            "various", "multiple", "several", "many", "some", "often", "usually",
            "typically", "generally", "commonly", "frequently", "regularly"
        ]
        
        self.specific_indicators = [
            r"\d+(\.\d+)?%",  # Percentages
            r"\d+(\.\d+)?\s*(ms|seconds|minutes|hours|days|weeks|months)",  # Time
            r"\d+(\.\d+)?\s*(MB|GB|TB|KB)",  # Data sizes
            r"\$\d+",  # Money
            r"\d+\s*(users|requests|transactions|calls)",  # Volumes
            r"\d+x\s*(faster|slower|more|less)",  # Multipliers
            r"version\s+\d+",  # Version numbers
        ]
    
    def analyze_specificity(self, response: str) -> Tuple[float, List[str]]:
        """Calculate specificity score and identify vague language"""
        issues = []
        
        # Count vague phrases
        vague_count = 0
        for phrase in self.vague_phrases:
            vague_count += len(re.findall(r'\b' + phrase + r'\b', response, re.IGNORECASE))
        
        # Count specific indicators
        specific_count = 0
        for pattern in self.specific_indicators:
            specific_count += len(re.findall(pattern, response, re.IGNORECASE))
        
        # Calculate word count
        word_count = len(response.split())
        
        # Calculate specificity score
        vague_ratio = vague_count / max(word_count / 100, 1)  # Vague phrases per 100 words
        specific_ratio = specific_count / max(word_count / 100, 1)  # Specific indicators per 100 words
        
        specificity_score = max(0.0, min(1.0, specific_ratio - (vague_ratio * 0.5)))
        
        # Generate issues
        if vague_ratio > 3:  # More than 3 vague phrases per 100 words
            issues.append(f"High use of vague language ({vague_count} vague phrases in {word_count} words)")
        
        if specific_count == 0:
            issues.append("No specific metrics, numbers, or concrete examples provided")
        
        return specificity_score, issues

class RelevanceAnalyzer:
    """Analyzes response relevance to the question"""
    
    def __init__(self):
        self.question_types = {
            "experience": ["experience", "background", "tell me about", "walk me through"],
            "technical": ["how", "what", "explain", "describe", "implement"],
            "behavioral": ["time when", "example of", "situation", "challenge"],
            "project": ["project", "built", "developed", "created", "designed"]
        }
    
    def analyze_relevance(self, question: str, response: str) -> Tuple[float, List[str]]:
        """Calculate relevance score based on question-response alignment"""
        issues = []
        
        # Identify question type
        question_type = self._identify_question_type(question)
        
        # Extract key concepts from question
        question_keywords = self._extract_keywords(question)
        
        # Check if response addresses the question
        relevance_score = self._calculate_semantic_overlap(question, response)
        
        # Check for response structure appropriateness
        structure_score = self._validate_response_structure(question_type, response)
        
        # Combine scores
        final_score = (relevance_score * 0.7) + (structure_score * 0.3)
        
        # Generate issues
        if relevance_score < 0.6:
            issues.append("Response doesn't adequately address the question")
        
        if structure_score < 0.5:
            issues.append(f"Response structure doesn't match {question_type} question type")
        
        return final_score, issues
    
    def _identify_question_type(self, question: str) -> str:
        """Identify the type of interview question"""
        question_lower = question.lower()
        
        for q_type, keywords in self.question_types.items():
            if any(keyword in question_lower for keyword in keywords):
                return q_type
        
        return "general"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Simple keyword extraction - in production, use more sophisticated NLP
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "about", "how", "what", "when", "where", "why"}
        return [word for word in words if word not in stop_words and len(word) > 3]
    
    def _calculate_semantic_overlap(self, question: str, response: str) -> float:
        """Calculate semantic overlap between question and response"""
        question_keywords = set(self._extract_keywords(question))
        response_keywords = set(self._extract_keywords(response))
        
        if not question_keywords:
            return 1.0
        
        overlap = len(question_keywords.intersection(response_keywords))
        return overlap / len(question_keywords)
    
    def _validate_response_structure(self, question_type: str, response: str) -> float:
        """Validate if response structure matches question type"""
        response_lower = response.lower()
        
        structure_indicators = {
            "experience": ["my experience", "i worked", "at [company]", "my role"],
            "technical": ["the approach", "implementation", "solution", "method"],
            "behavioral": ["situation", "task", "action", "result", "challenge"],
            "project": ["project", "built", "developed", "implemented", "architecture"]
        }
        
        expected_indicators = structure_indicators.get(question_type, [])
        found_indicators = sum(1 for indicator in expected_indicators if indicator in response_lower)
        
        return found_indicators / max(len(expected_indicators), 1)

class StreamingQualityController:
    """Real-time quality control during streaming generation"""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.MODERATE):
        self.validation_level = validation_level
        self.fact_checker = TechnicalFactChecker()
        self.specificity_analyzer = SpecificityAnalyzer()
        self.relevance_analyzer = RelevanceAnalyzer()
        
        # Quality thresholds by validation level
        self.thresholds = {
            ValidationLevel.STRICT: {"overall": 0.8, "authenticity": 0.9, "specificity": 0.7},
            ValidationLevel.MODERATE: {"overall": 0.6, "authenticity": 0.7, "specificity": 0.5},
            ValidationLevel.PERMISSIVE: {"overall": 0.4, "authenticity": 0.5, "specificity": 0.3}
        }
    
    def validate_streaming_response(self, question: str, response_generator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Validate response quality during streaming generation"""
        accumulated_response = ""
        token_count = 0
        
        for token in response_generator:
            accumulated_response += token
            token_count += 1
            
            # Periodic quality checks (every 50 tokens)
            if token_count % 50 == 0:
                quality_issues = self._quick_quality_check(accumulated_response)
                if quality_issues:
                    # Log issues but continue streaming
                    self._log_quality_issue(f"Token {token_count}: {quality_issues[0]}")
            
            yield token
        
        # Final comprehensive validation
        final_metrics = self.comprehensive_validation(question, accumulated_response)
        self._handle_final_validation(final_metrics)
    
    def comprehensive_validation(self, question: str, response: str) -> QualityMetrics:
        """Perform comprehensive quality validation"""
        
        # Technical fact checking
        is_technically_valid, tech_issues = self.fact_checker.validate_technical_content(response)
        authenticity_score = 1.0 if is_technically_valid else max(0.0, 1.0 - (len(tech_issues) * 0.2))
        
        # Specificity analysis
        specificity_score, specificity_issues = self.specificity_analyzer.analyze_specificity(response)
        
        # Relevance analysis
        relevance_score, relevance_issues = self.relevance_analyzer.analyze_relevance(question, response)
        
        # Calculate confidence score based on response characteristics
        confidence_score = self._calculate_confidence_score(response)
        
        # Calculate overall score
        overall_score = (
            authenticity_score * 0.3 +
            specificity_score * 0.25 +
            relevance_score * 0.25 +
            confidence_score * 0.2
        )
        
        # Combine all issues
        all_issues = tech_issues + specificity_issues + relevance_issues
        
        # Generate suggestions
        suggestions = self._generate_suggestions(authenticity_score, specificity_score, relevance_score)
        
        return QualityMetrics(
            confidence_score=confidence_score,
            specificity_score=specificity_score,
            relevance_score=relevance_score,
            authenticity_score=authenticity_score,
            overall_score=overall_score,
            issues=all_issues,
            suggestions=suggestions
        )
    
    def _quick_quality_check(self, partial_response: str) -> List[str]:
        """Quick quality check during streaming"""
        issues = []
        
        # Check for immediate red flags
        red_flags = [
            "I'd be happy to",
            "Thank you for having me",
            "Here's a simplified example:",
            "```python\n# Example"
        ]
        
        for flag in red_flags:
            if flag in partial_response:
                issues.append(f"Generic/fabricated content detected: {flag}")
        
        return issues
    
    def _calculate_confidence_score(self, response: str) -> float:
        """Calculate confidence score based on response characteristics"""
        score = 1.0
        
        # Check for uncertainty indicators
        uncertainty_phrases = [
            "i think", "maybe", "possibly", "i believe", "not sure",
            "i assume", "probably", "might be", "could be"
        ]
        
        uncertainty_count = sum(1 for phrase in uncertainty_phrases 
                              if phrase in response.lower())
        
        # Reduce score for uncertainty
        score -= uncertainty_count * 0.1
        
        # Check for confidence indicators
        confidence_phrases = [
            "in my experience", "i've implemented", "i've built",
            "at mastercard", "at john deere", "specific result"
        ]
        
        confidence_count = sum(1 for phrase in confidence_phrases 
                             if phrase in response.lower())
        
        # Increase score for confidence indicators
        score += confidence_count * 0.05
        
        return max(0.0, min(1.0, score))
    
    def _generate_suggestions(self, auth_score: float, spec_score: float, rel_score: float) -> List[str]:
        """Generate improvement suggestions based on scores"""
        suggestions = []
        
        if auth_score < 0.7:
            suggestions.append("Include more specific examples from your actual experience")
            suggestions.append("Reference specific companies, projects, or technologies you've worked with")
        
        if spec_score < 0.6:
            suggestions.append("Add concrete metrics, percentages, or measurable outcomes")
            suggestions.append("Replace vague language with specific technical details")
        
        if rel_score < 0.7:
            suggestions.append("Ensure your response directly addresses the question asked")
            suggestions.append("Structure your answer appropriately for the question type")
        
        return suggestions
    
    def _log_quality_issue(self, issue: str):
        """Log quality issue for monitoring"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[QUALITY ALERT {timestamp}] {issue}")
    
    def _handle_final_validation(self, metrics: QualityMetrics):
        """Handle final validation results"""
        current_thresholds = self.thresholds[self.validation_level]
        
        if metrics.overall_score < current_thresholds["overall"]:
            print(f"\n[QUALITY WARNING] Overall score: {metrics.overall_score:.2f} (below threshold: {current_thresholds['overall']})")
            
            if metrics.issues:
                print("Issues detected:")
                for issue in metrics.issues:
                    print(f"  • {issue}")
            
            if metrics.suggestions:
                print("Suggestions for improvement:")
                for suggestion in metrics.suggestions:
                    print(f"  → {suggestion}")
        
        # Log metrics for analysis
        self._log_metrics(metrics)
    
    def _log_metrics(self, metrics: QualityMetrics):
        """Log metrics for analysis and improvement"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": metrics.overall_score,
            "authenticity_score": metrics.authenticity_score,
            "specificity_score": metrics.specificity_score,
            "relevance_score": metrics.relevance_score,
            "confidence_score": metrics.confidence_score,
            "issues_count": len(metrics.issues),
            "suggestions_count": len(metrics.suggestions)
        }
        
        # In production, send to logging service
        # For now, just print for debugging
        print(f"[METRICS] {json.dumps(log_entry, indent=2)}")

# Usage example and integration helper
class QualityEnhancedGenerator:
    """Wrapper that adds quality control to any response generator"""
    
    def __init__(self, base_generator, validation_level: ValidationLevel = ValidationLevel.MODERATE):
        self.base_generator = base_generator
        self.quality_controller = StreamingQualityController(validation_level)
    
    def generate_with_quality_control(self, question: str, *args, **kwargs):
        """Generate response with real-time quality control"""
        base_response_gen = self.base_generator(question, *args, **kwargs)
        return self.quality_controller.validate_streaming_response(question, base_response_gen)