"""Pre-warm Ollama model before interview"""
import subprocess
import sys

def warmup():
    model = "llama3.2:3b"
    print(f"Warming up {model}...")
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model, 'test'],
            capture_output=True,
            timeout=10,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ {model} ready!")
            return True
        else:
            print(f"✗ Warmup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = warmup()
    sys.exit(0 if success else 1)