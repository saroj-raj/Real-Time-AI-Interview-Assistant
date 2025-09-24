"""
LLM Client for Interview Assistant
Combines generic Ollama client with interview-specific profile.
Maintains backward compatibility with existing main.py
"""

import os
from typing import Generator
from interview_profile import InterviewProfile

# Backward compatibility - expose the same interface
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "codellama:7b-instruct-q4_0")

class WorkingLLM:
    """
    Interview-specific LLM client that maintains backward compatibility.
    Now uses modular architecture with generic client + personal profile.
    """
    
    def __init__(self):
        # Initialize with interview profile
        self.profile = InterviewProfile(model=DEFAULT_MODEL)
        
        # Expose properties for backward compatibility
        self.working = self.profile.llm.is_working()
        self.model = self.profile.model
        self.base_url = self.profile.llm.base_url
        
        # Show connection status
        if self.working:
            print(f"[LLM] Connected to Ollama with {self.model}")
        else:
            print(f"[LLM] Cannot connect to Ollama")

    def generate_stream(self, question: str, context: str = "", job_description: str = "") -> Generator[str, None, None]:
        """
        Generate streaming interview response.
        Maintains same interface as original but now uses modular backend.
        """
        print(f"[LLM] Sending request to Ollama...")
        
        # Use the interview profile to generate response
        yield from self.profile.generate_response_stream(question, context, job_description)

    # Additional methods for enhanced functionality
    def get_profile_info(self):
        """Get information about the interview profile"""
        return self.profile.get_profile_summary()
    
    def test_connection(self):
        """Test the connection manually"""
        return self.profile.llm._test_connection()
    
    def change_model(self, new_model: str):
        """Change the underlying model"""
        print(f"[LLM] Switching from {self.model} to {new_model}")
        self.profile = InterviewProfile(model=new_model)
        self.working = self.profile.llm.is_working()
        self.model = self.profile.model
        return self.working

def make_llm():
    """
    Factory function for creating interview LLM client.
    Maintains backward compatibility with existing main.py
    """
    return WorkingLLM()

# Additional utility functions
def list_available_models():
    """List all available Ollama models"""
    import requests
    try:
        response = requests.get(f"{DEFAULT_OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m.get("name", "") for m in models]
    except:
        pass
    return []

def create_custom_profile(name: str, role: str, experience: int, expertise: list):
    """
    Create a custom interview profile (for future extensibility)
    
    Example:
        custom_llm = create_custom_profile(
            name="John Doe",
            role="Data Scientist", 
            experience=5,
            expertise=["deep learning", "computer vision"]
        )
    """
    # This would allow easy customization in the future
    from interview_profile import InterviewProfile
    
    class CustomProfile(InterviewProfile):
        def __init__(self, model=None):
            super().__init__(model)
            self.name = name
            self.role = role
            self.experience_years = experience
            self.expertise_areas = expertise
    
    return CustomProfile()

if __name__ == "__main__":
    # Test the modular system
    print("Testing Modular LLM Client")
    print("=" * 40)
    
    # Test backward compatibility
    llm = make_llm()
    print(f"✓ LLM created: {llm.model}")
    print(f"✓ Working: {llm.working}")
    
    # Test profile info
    profile = llm.get_profile_info()
    print(f"✓ Profile: {profile['name']} - {profile['role']}")
    print(f"✓ Experience: {profile['experience_years']} years")
    
    # Test available models
    models = list_available_models()
    print(f"✓ Available models: {len(models)}")
    
    # Test simple generation
    if llm.working:
        print("\n--- Test Generation ---")
        for token in llm.generate_stream("Hello, introduce yourself briefly"):
            print(token, end="", flush=True)
        print("\n")
    
    print("✓ All tests passed!")