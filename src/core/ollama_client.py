"""
Generic Ollama LLM Client
Handles connection, streaming, and error management for any Ollama model.
"""
import os
import json
import requests
from typing import Generator, Optional, Dict, Any

DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")

class OllamaClient:
    """Generic Ollama client for any model and use case"""
    
    def __init__(self, model: str, base_url: str = DEFAULT_OLLAMA_URL):
        self.base_url = base_url
        self.model = model
        self.working = self._test_connection()
        
        if self.working:
            print(f"[LLM] Connected to Ollama with {self.model}")
        else:
            print(f"[LLM] Failed to connect to Ollama")

    def _test_connection(self) -> bool:
        """Test if Ollama server and model are available"""
        try:
            # Check server
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"[LLM] Server error: {response.status_code}")
                return False
            
            # Check model availability
            models = response.json().get("models", [])
            available_models = [m.get("name", "") for m in models]
            
            if self.model not in available_models:
                print(f"[LLM] Model '{self.model}' not found")
                print(f"[LLM] Available: {available_models}")
                return False
            
            # Test generation
            test_response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"num_predict": 5}
                },
                timeout=10
            )
            
            if test_response.status_code == 500:
                error_data = test_response.json()
                if "memory" in error_data.get("error", "").lower():
                    print(f"[LLM] Memory error: {error_data['error']}")
                    return False
                print(f"[LLM] Server error: {error_data.get('error', 'Unknown')}")
                return False
            elif test_response.status_code != 200:
                print(f"[LLM] Generation test failed: {test_response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"[LLM] Connection error: {e}")
            return False

    def generate_stream(self, 
                       prompt: str, 
                       options: Optional[Dict[str, Any]] = None,
                       fallback_response: Optional[str] = None) -> Generator[str, None, None]:
        """
        Generate streaming response from Ollama
        
        Args:
            prompt: The prompt to send to the model
            options: Ollama generation options (temperature, num_predict, etc.)
            fallback_response: Response to return if generation fails
        """
        if not self.working:
            print("[LLM] Ollama not available")
            if fallback_response:
                yield fallback_response
            return
        
        # Default options
        default_options = {
            "temperature": 0.3,
            "num_ctx": 3072,
            "num_predict": 800,
            "top_p": 0.9
        }
        
        if options:
            default_options.update(options)
        
        try:
            print("[LLM] Generating response...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": default_options
                },
                stream=True,
                timeout=60
            )
            
            if response.status_code == 500:
                error_data = response.json()
                print(f"[LLM] Server error: {error_data.get('error', 'Unknown')}")
                if fallback_response:
                    yield fallback_response
                return
            elif response.status_code != 200:
                print(f"[LLM] HTTP error: {response.status_code}")
                if fallback_response:
                    yield fallback_response
                return
            
            print("[LLM] Streaming response...")
            token_count = 0
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        # Handle API errors
                        if 'error' in data:
                            print(f"[LLM] API error: {data['error']}")
                            if token_count == 0 and fallback_response:
                                yield fallback_response
                            return
                        
                        # Yield tokens
                        if 'response' in data and data['response']:
                            token_count += 1
                            yield data['response']
                        
                        # Check completion
                        if data.get('done', False):
                            print(f"[LLM] Complete ({token_count} tokens)")
                            return
                            
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"[LLM] Stream processing error: {e}")
                        continue
            
            # No tokens received
            if token_count == 0:
                print("[LLM] No response received")
                if fallback_response:
                    yield fallback_response
                    
        except requests.exceptions.Timeout:
            print("[LLM] Request timeout")
            if fallback_response:
                yield fallback_response
        except Exception as e:
            print(f"[LLM] Generation failed: {e}")
            if fallback_response:
                yield fallback_response

    def generate_simple(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate a simple non-streaming response"""
        if not self.working:
            return "LLM not available"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": max_tokens}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Generation failed: {e}"

    def is_working(self) -> bool:
        """Check if the client is working"""
        return self.working

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if not self.working:
            return {"model": self.model, "status": "unavailable"}
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                for model in models:
                    if model.get("name") == self.model:
                        return {
                            "model": self.model,
                            "status": "available",
                            "size": model.get("size", 0),
                            "modified": model.get("modified_at", "unknown")
                        }
            return {"model": self.model, "status": "not_found"}
        except:
            return {"model": self.model, "status": "error"}