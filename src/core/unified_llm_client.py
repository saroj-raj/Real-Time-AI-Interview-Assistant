"""
Unified LLM Client - Supports Groq API and Ollama
Auto-detects best available option with intelligent fallback
"""
import os
import json
import requests
from typing import Generator, Optional, Dict, Any
import time

# Configuration
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class UnifiedLLMClient:
    """Unified client supporting both Groq and Ollama with intelligent fallback"""
    
    def __init__(self, model: str, prefer_groq: bool = True):
        self.model = model
        self.provider = None
        self.working = False
        
        # Map common model names to Groq equivalents
        self.groq_model_map = {
            "llama3.2:3b": "llama-3.2-3b-preview",
            "llama3.1:8b": "llama-3.1-8b-instant",
            "llama3:70b": "llama-3.1-70b-versatile",
            "mistral:7b": "mixtral-8x7b-32768",
            "mixtral": "mixtral-8x7b-32768",
        }
        
        # Try Groq first if preferred and API key available
        if prefer_groq and GROQ_API_KEY:
            if self._init_groq():
                return
        
        # Fallback to Ollama
        self._init_ollama()
    
    def _init_groq(self) -> bool:
        """Initialize Groq API client"""
        if not GROQ_API_KEY:
            return False
        
        try:
            # Map model name to Groq equivalent
            groq_model = self.groq_model_map.get(self.model, "llama-3.2-3b-preview")
            
            # Test Groq API
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            test_data = {
                "model": groq_model,
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10,
                "temperature": 0.5
            }
            
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.provider = "groq"
                self.groq_model = groq_model
                self.groq_headers = headers
                self.working = True
                print(f"✓ [LLM] Connected to Groq API with {groq_model}")
                return True
            else:
                error_detail = response.text[:200] if response.text else "No details"
                print(f"[LLM] Groq API test failed: {response.status_code}")
                print(f"[LLM] Error: {error_detail}")
                
                # Try alternative model
                if "llama-3.2" in groq_model:
                    alt_model = "llama-3.1-8b-instant"
                    print(f"[LLM] Trying alternative model: {alt_model}")
                    test_data["model"] = alt_model
                    
                    alt_response = requests.post(
                        GROQ_API_URL,
                        headers=headers,
                        json=test_data,
                        timeout=10
                    )
                    
                    if alt_response.status_code == 200:
                        self.provider = "groq"
                        self.groq_model = alt_model
                        self.groq_headers = headers
                        self.working = True
                        print(f"✓ [LLM] Connected to Groq API with {alt_model}")
                        return True
                
                return False
                
        except Exception as e:
            print(f"[LLM] Groq initialization failed: {str(e)[:100]}")
            return False
    
    def _init_ollama(self) -> bool:
        """Initialize Ollama client"""
        self.ollama_url = DEFAULT_OLLAMA_URL
        
        try:
            # Test Ollama connection
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            if response.status_code != 200:
                print(f"[LLM] ✗ Ollama not available")
                return False
            
            # Check model availability
            models_data = response.json().get("models", [])
            available_models = [m.get("name", "") for m in models_data]
            
            if self.model not in available_models:
                # Try partial match
                matching = [m for m in available_models if self.model in m or m in self.model]
                if matching:
                    self.model = matching[0]
                else:
                    print(f"[LLM] Model '{self.model}' not found in Ollama")
                    return False
            
            # Quick test
            test_response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "Hi",
                    "stream": False,
                    "options": {"num_predict": 3}
                },
                timeout=8
            )
            
            if test_response.status_code == 200:
                self.provider = "ollama"
                self.working = True
                print(f"✓ [LLM] Connected to Ollama with {self.model}")
                return True
            
            return False
            
        except Exception as e:
            print(f"[LLM] Ollama initialization failed: {str(e)[:100]}")
            return False
    
    def generate_stream(self, 
                       prompt: str, 
                       options: Optional[Dict[str, Any]] = None,
                       fallback_response: Optional[str] = None) -> Generator[str, None, None]:
        """
        Generate streaming response from best available provider
        """
        if not self.working:
            print("[LLM] ⚠ No LLM provider available - using fallback")
            if fallback_response:
                yield fallback_response
            return
        
        if self.provider == "groq":
            yield from self._generate_groq_stream(prompt, options, fallback_response)
        elif self.provider == "ollama":
            yield from self._generate_ollama_stream(prompt, options, fallback_response)
    
    def _generate_groq_stream(self,
                             prompt: str,
                             options: Optional[Dict[str, Any]] = None,
                             fallback_response: Optional[str] = None) -> Generator[str, None, None]:
        """Generate streaming response from Groq API"""
        try:
            print(f"[LLM] ⚡ Generating with Groq ({self.groq_model})...")
            start_time = time.time()
            
            # Parse options
            temperature = options.get("temperature", 0.3) if options else 0.3
            max_tokens = options.get("num_predict", 400) if options else 300
            
            # Prepare request
            data = {
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            response = requests.post(
                GROQ_API_URL,
                headers=self.groq_headers,
                json=data,
                stream=True,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"[LLM] ✗ Groq API error: {response.status_code}")
                if fallback_response:
                    yield fallback_response
                return
            
            token_count = 0
            first_token_time = None
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]  # Remove 'data: ' prefix
                        
                        if line == '[DONE]':
                            break
                        
                        try:
                            chunk = json.loads(line)
                            delta = chunk['choices'][0]['delta']
                            
                            if 'content' in delta:
                                if token_count == 0:
                                    first_token_time = time.time()
                                    ttft = first_token_time - start_time
                                    print(f"[LLM] ⚡ First token: {ttft:.2f}s")
                                
                                token_count += 1
                                yield delta['content']
                        except json.JSONDecodeError:
                            continue
            
            total_time = time.time() - start_time
            tokens_per_sec = token_count / total_time if total_time > 0 else 0
            print(f"[LLM] ✓ Complete: {token_count} tokens in {total_time:.2f}s ({tokens_per_sec:.1f} t/s)")
            
        except requests.exceptions.Timeout:
            print("[LLM] ✗ Groq API timeout")
            if fallback_response:
                yield fallback_response
        except Exception as e:
            print(f"[LLM] ✗ Groq generation failed: {str(e)[:100]}")
            if fallback_response:
                yield fallback_response
    
    def _generate_ollama_stream(self,
                               prompt: str,
                               options: Optional[Dict[str, Any]] = None,
                               fallback_response: Optional[str] = None) -> Generator[str, None, None]:
        """Generate streaming response from Ollama"""
        try:
            print(f"[LLM] ⚡ Generating with Ollama ({self.model})...")
            start_time = time.time()
            
            # Optimized defaults
            default_options = {
                "temperature": 0.3,
                "num_ctx": 2048,
                "num_predict": 400,
                "top_p": 0.9,
                "num_thread": 16,
            }
            
            if options:
                default_options.update(options)
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": default_options
                },
                stream=True,
                timeout=45
            )
            
            if response.status_code != 200:
                print(f"[LLM] ✗ Ollama error: {response.status_code}")
                if fallback_response:
                    yield fallback_response
                return
            
            token_count = 0
            first_token_time = None
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        if 'error' in data:
                            print(f"[LLM] ✗ API error: {data['error']}")
                            if token_count == 0 and fallback_response:
                                yield fallback_response
                            return
                        
                        if 'response' in data and data['response']:
                            if token_count == 0:
                                first_token_time = time.time()
                                ttft = first_token_time - start_time
                                print(f"[LLM] ⚡ First token: {ttft:.2f}s")
                            
                            token_count += 1
                            yield data['response']
                        
                        if data.get('done', False):
                            total_time = time.time() - start_time
                            tokens_per_sec = token_count / total_time if total_time > 0 else 0
                            print(f"[LLM] ✓ Complete: {token_count} tokens in {total_time:.2f}s ({tokens_per_sec:.1f} t/s)")
                            return
                    except json.JSONDecodeError:
                        continue
            
            if token_count == 0:
                print("[LLM] ✗ No response tokens received")
                if fallback_response:
                    yield fallback_response
                    
        except Exception as e:
            print(f"[LLM] ✗ Ollama generation failed: {str(e)[:100]}")
            if fallback_response:
                yield fallback_response
    
    def is_working(self) -> bool:
        """Check if client is working"""
        return self.working
    
    def get_provider(self) -> str:
        """Get current provider name"""
        return self.provider if self.working else "none"


# Backward compatibility - alias to OllamaClient
OllamaClient = UnifiedLLMClient


def test_client():
    """Test the unified client"""
    print(f"\n{'='*60}")
    print("Testing Unified LLM Client")
    print(f"{'='*60}\n")
    
    # Test with default model
    client = UnifiedLLMClient("llama3.2:3b")
    
    if not client.is_working():
        print("✗ No LLM provider available")
        print("\nSetup instructions:")
        print("Option 1 (Groq - FAST): Set GROQ_API_KEY environment variable")
        print("Option 2 (Ollama - LOCAL): Run 'ollama serve' and 'ollama pull llama3.2:3b'")
        return False
    
    print(f"✓ Using provider: {client.get_provider()}")
    
    # Test generation
    print("\n" + "="*60)
    print("Testing Generation")
    print("="*60 + "\n")
    
    test_prompt = "Say hello in 10 words."
    fallback = "Hello! I'm an AI assistant ready to help."
    
    print("Response: ", end="", flush=True)
    for token in client.generate_stream(test_prompt, fallback_response=fallback):
        print(token, end="", flush=True)
    print("\n")
    
    print("\n✅ Test complete!")
    return True


if __name__ == "__main__":
    test_client()