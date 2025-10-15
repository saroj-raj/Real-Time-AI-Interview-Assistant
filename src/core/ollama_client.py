"""
Optimized Ollama LLM Client for Interview Assistant
Fast, reliable connection with intelligent fallback handling
"""
import os
import json
import requests
from typing import Generator, Optional, Dict, Any
import time

DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")

class OllamaClient:
    """Optimized Ollama client for fast interview responses"""
    
    def __init__(self, model: str, base_url: str = DEFAULT_OLLAMA_URL):
        self.base_url = base_url
        self.model = model
        self.working = False
        self.connection_attempts = 0
        self.max_retries = 2
        
        # Try to connect with retries
        for attempt in range(self.max_retries):
            self.connection_attempts = attempt + 1
            self.working = self._test_connection()
            if self.working:
                break
            if attempt < self.max_retries - 1:
                print(f"[LLM] Retrying connection... ({attempt + 1}/{self.max_retries})")
                time.sleep(0.5)
        
        if self.working:
            print(f"✓ [LLM] Connected to Ollama with {self.model}")
        else:
            print(f"✗ [LLM] Ollama not available - using fallback responses")

    def _test_connection(self) -> bool:
        """Test if Ollama server and model are available"""
        try:
            # Check server with short timeout
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code != 200:
                print(f"[LLM] Server returned status {response.status_code}")
                return False
            
            # Check model availability
            models_data = response.json().get("models", [])
            available_models = [m.get("name", "") for m in models_data]
            
            # Debug: show what we're looking for vs what's available
            if self.model not in available_models:
                print(f"[LLM] Model '{self.model}' not in available models")
                print(f"[LLM] Available models: {available_models}")
                
                # Try to match partial names (e.g., "llama3.2:3b" matches "llama3.2:3b")
                matching_models = [m for m in available_models if self.model in m or m in self.model]
                if matching_models:
                    print(f"[LLM] Found similar model: {matching_models[0]}")
                    self.model = matching_models[0]  # Use the matching model
                else:
                    return False
            
            # Quick generation test with minimal tokens
            test_response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "Hi",
                    "stream": False,
                    "options": {"num_predict": 3, "temperature": 0.1}
                },
                timeout=8
            )
            
            if test_response.status_code == 500:
                error_data = test_response.json()
                error_msg = error_data.get("error", "")
                if "memory" in error_msg.lower():
                    print(f"[LLM] ⚠ Memory error - model may be too large")
                elif "not found" in error_msg.lower():
                    print(f"[LLM] ⚠ Model not found: {error_msg}")
                else:
                    print(f"[LLM] ⚠ Server error: {error_msg}")
                return False
            elif test_response.status_code != 200:
                print(f"[LLM] Generation test failed with status {test_response.status_code}")
                return False
            
            # Verify we got a response
            response_text = test_response.json().get("response", "")
            if not response_text:
                print("[LLM] ⚠ Model returned empty response")
                return False
            
            print(f"[LLM] ✓ Model test successful")
            return True
            
        except requests.exceptions.Timeout:
            print("[LLM] ⚠ Connection timeout - Ollama may be slow or unresponsive")
            return False
        except requests.exceptions.ConnectionError:
            print("[LLM] ⚠ Cannot connect to Ollama - is it running? (ollama serve)")
            return False
        except Exception as e:
            print(f"[LLM] ⚠ Connection test failed: {str(e)[:100]}")
            return False

    def generate_stream(self, 
                       prompt: str, 
                       options: Optional[Dict[str, Any]] = None,
                       fallback_response: Optional[str] = None) -> Generator[str, None, None]:
        """
        Generate streaming response from Ollama with optimized settings
        
        Args:
            prompt: The prompt to send to the model
            options: Ollama generation options (temperature, num_predict, etc.)
            fallback_response: Response to return if generation fails
        """
        if not self.working:
            print("[LLM] ⚠ Ollama not available - using fallback")
            if fallback_response:
                yield fallback_response
            return
        
        # OPTIMIZED defaults for SPEED
        default_options = {
            "temperature": 0.3,      # Low for consistency
            "num_ctx": 512,         # Reduced context for speed
            "num_predict": 100,      # Shorter responses = faster
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_thread": 8,         # Use multiple CPU cores
        }
        
        # Override with custom options
        if options:
            default_options.update(options)
        
        try:
            print(f"[LLM] ⚡ Generating with {self.model}...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": default_options
                },
                stream=True,
                timeout=45  # Shorter timeout for faster failure
            )
            
            # Handle HTTP errors
            if response.status_code == 500:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Unknown error')
                    print(f"[LLM] ✗ Server error: {error_msg}")
                except:
                    print(f"[LLM] ✗ Server error (status 500)")
                
                if fallback_response:
                    yield fallback_response
                return
                
            elif response.status_code != 200:
                print(f"[LLM] ✗ HTTP {response.status_code}")
                if fallback_response:
                    yield fallback_response
                return
            
            # Stream response tokens
            token_count = 0
            first_token_time = None
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        # Handle API errors
                        if 'error' in data:
                            print(f"[LLM] ✗ API error: {data['error']}")
                            if token_count == 0 and fallback_response:
                                yield fallback_response
                            return
                        
                        # Yield tokens
                        if 'response' in data and data['response']:
                            if token_count == 0:
                                first_token_time = time.time()
                                ttft = first_token_time - start_time
                                print(f"[LLM] ⚡ First token: {ttft:.2f}s")
                            
                            token_count += 1
                            yield data['response']
                        
                        # Check completion
                        if data.get('done', False):
                            total_time = time.time() - start_time
                            tokens_per_sec = token_count / total_time if total_time > 0 else 0
                            print(f"[LLM] ✓ Complete: {token_count} tokens in {total_time:.2f}s ({tokens_per_sec:.1f} t/s)")
                            return
                            
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"[LLM] ⚠ Stream error: {str(e)[:100]}")
                        continue
            
            # No tokens received - use fallback
            if token_count == 0:
                print("[LLM] ✗ No response tokens received")
                if fallback_response:
                    yield fallback_response
                    
        except requests.exceptions.Timeout:
            print("[LLM] ✗ Request timeout (45s)")
            if fallback_response:
                yield fallback_response
        except requests.exceptions.ConnectionError:
            print("[LLM] ✗ Connection lost during generation")
            self.working = False  # Mark as not working
            if fallback_response:
                yield fallback_response
        except Exception as e:
            print(f"[LLM] ✗ Generation failed: {str(e)[:100]}")
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
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.3,
                        "num_thread": 8
                    }
                },
                timeout=20
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Generation failed: {str(e)[:100]}"

    def warm_up(self):
        """Pre-warm the model by running a quick generation"""
        if not self.working:
            return False
        
        print(f"[LLM] 🔥 Warming up {self.model}...")
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"num_predict": 5}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("[LLM] ✓ Model warmed up and ready")
                return True
            else:
                print(f"[LLM] ⚠ Warmup failed: status {response.status_code}")
                return False
        except Exception as e:
            print(f"[LLM] ⚠ Warmup error: {str(e)[:100]}")
            return False

    def is_working(self) -> bool:
        """Check if the client is working"""
        return self.working

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if not self.working:
            return {
                "model": self.model,
                "status": "unavailable",
                "message": "Ollama not connected"
            }
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get("models", [])
                for model in models:
                    if model.get("name") == self.model:
                        size_gb = model.get("size", 0) / (1024**3)
                        return {
                            "model": self.model,
                            "status": "available",
                            "size": f"{size_gb:.1f} GB",
                            "modified": model.get("modified_at", "unknown")
                        }
            return {
                "model": self.model,
                "status": "not_found",
                "message": f"Model {self.model} not in available models"
            }
        except Exception as e:
            return {
                "model": self.model,
                "status": "error",
                "message": str(e)[:100]
            }

    def list_available_models(self) -> list:
        """List all available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [
                    {
                        "name": m.get("name"),
                        "size": f"{m.get('size', 0) / (1024**3):.1f} GB"
                    }
                    for m in models
                ]
        except:
            pass
        return []


# Convenience function for testing
def test_client(model: str = "llama3.2:3b"):
    """Test the Ollama client"""
    print(f"\n{'='*60}")
    print(f"Testing Ollama Client with {model}")
    print(f"{'='*60}\n")
    
    client = OllamaClient(model)
    
    if not client.is_working():
        print("\n❌ Client not working - check Ollama service")
        print("\nTroubleshooting:")
        print("1. Is Ollama running? Try: ollama serve")
        print("2. Is the model downloaded? Try: ollama list")
        print(f"3. Pull the model if needed: ollama pull {model}")
        return False
    
    # Show model info
    info = client.get_model_info()
    print(f"\n✓ Model Info: {info}")
    
    # Test warmup
    client.warm_up()
    
    # Test generation
    print("\n" + "="*60)
    print("Testing Generation")
    print("="*60 + "\n")
    
    test_prompt = "Tell me about yourself in 30 words."
    fallback = "I am an AI assistant ready to help with your interview preparation."
    
    print("Response: ", end="", flush=True)
    for token in client.generate_stream(test_prompt, fallback_response=fallback):
        print(token, end="", flush=True)
    print("\n")
    
    print("\n✅ Test complete!")
    return True


if __name__ == "__main__":
    # Run test when executed directly
    test_client()