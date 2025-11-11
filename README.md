# Real-Time AI Interview Assistant

A comprehensive AI-powered interview practice system that provides personalized, context-aware responses based on your professional background and target roles. Features real-time audio capture, transcription, and streaming LLM responses optimized for technical interviews.

## Features

### Core Capabilities
- **Real-time Audio Processing**: Manual start/stop recording with Whisper transcription
- **Profile-Based Responses**: Personalized answers based on your experience and target role
- **Streaming LLM Integration**: Cloud (Groq) or Local (Ollama) inference with real-time word wrapping
- **Job Description Alignment**: Responses tailored to specific job requirements
- **Multi-User Support**: Individual profiles for different users and roles
- **Cross-Platform Audio**: Windows WASAPI loopback and virtual audio device support
- **Dual LLM Support**: Fast cloud inference with Groq or privacy-focused local Ollama

### Technical Features
- **Modular Architecture**: Clean separation between core components and user profiles
- **Audio Device Detection**: Automatic system audio and virtual device detection
- **Response Interruption**: Space key to stop LLM generation mid-response
- **Session Management**: Question numbering and interview flow control
- **Error Handling**: Comprehensive fallback mechanisms and error recovery
- **Smart LLM Routing**: Automatic fallback from Groq to Ollama if API unavailable

## Architecture

### System Design
```
Real-TimeAIInterviewAssistant/
├── main.py                    # Main application with profile selection
├── profiles/                  # User and role profiles
│   └── [user_name]/
│       ├── [role_name].py
│       └── [role_name]_job_description.txt
├── src/core/                  # Generic components
│   ├── ollama_client.py       # LLM interface
│   ├── audio_transcriber.py   # Whisper integration
│   └── audio_device_util.py   # Audio device management
├── my_context.txt            # General context file
├── job_description.txt       # Global job description fallback
└── requirements.txt
```

### Technology Stack
- **Audio**: OpenAI Whisper (large model) for transcription, sounddevice for capture
- **LLM**: Groq API (fast cloud) or Ollama (local privacy) with intelligent fallback
- **Language**: Python 3.8+ with minimal dependencies
- **Architecture**: Streaming responses with real-time processing

## Installation

### Prerequisites
- Python 3.8 or higher
- **Option 1 (Recommended - Fast)**: Groq API key ([Get free key](https://console.groq.com))
- **Option 2 (Local - Private)**: Ollama installed and running
- Audio input device (microphone or system audio setup)

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/Real-TimeAIInterviewAssistant.git
cd Real-TimeAIInterviewAssistant
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup LLM (Choose One)

**Option A: Groq API (Recommended - Faster)**
```bash
# Get free API key from https://console.groq.com
# Set environment variable
export GROQ_API_KEY="your_api_key_here"  # Linux/Mac
# OR
set GROQ_API_KEY=your_api_key_here  # Windows CMD
# OR
$env:GROQ_API_KEY="your_api_key_here"  # Windows PowerShell
```

**Option B: Ollama (Local - More Private)**
```bash
# Install Ollama from https://ollama.com
# Pull a recommended model
ollama pull llama3.2:3b
# OR
ollama pull llama3.1:8b
```

**The system automatically uses Groq if API key is set, otherwise falls back to Ollama.**

### Step 5: Create Your Profile
See [profiles/README.md](profiles/README.md) for detailed profile setup instructions.

## Quick Start

### Basic Usage
```bash
python main.py
```

The application will:
1. Display available users and roles
2. Load your profile and job description
3. Initialize audio devices and models
4. Start the interview session

### Interview Controls
- **ENTER**: Start/stop recording
- **SPACE**: Interrupt AI response generation
- **CTRL+C**: Exit application

### Example Session Flow
```
[Q1] Press ENTER to start recording...
🔴 RECORDING... (Press ENTER to stop)
⏹ Stopped (5.2s)
⚡ Transcribing...

🎤 QUESTION:
Tell me about your experience with distributed systems.

🤖 RESPONSE:
Based on my experience as a Senior Software Engineer, I've worked extensively 
with distributed systems at scale...
```

## Configuration

### Audio Setup

#### Windows - System Audio Capture
For capturing computer audio (not microphone):
1. **Option A**: Use PyAudioWPatch for WASAPI loopback
2. **Option B**: Install VB-Audio Virtual Cable
3. **Option C**: Enable "Stereo Mix" in sound settings

#### macOS - Virtual Audio Device
```bash
# Install BlackHole virtual audio device
brew install blackhole-2ch

# Create Multi-Output Device in Audio MIDI Setup
# Set as system output, record from BlackHole input
```

#### Linux - PulseAudio Monitor
```bash
# List audio sources
pactl list sources short

# Find monitor devices (usually end with .monitor)
# Use monitor device index in application
```

### Model Configuration

#### LLM Provider Selection
The system uses **Groq by default** (if `GROQ_API_KEY` is set), otherwise **falls back to Ollama**.

**Groq Models** (Cloud - Fast):
- `llama-3.2-3b-preview` (default, very fast)
- `llama-3.1-8b-instant` (higher quality)
- `mixtral-8x7b-32768` (best quality, longer context)

**Ollama Models** (Local - Private):
- `llama3.2:3b` (recommended, 2GB RAM)
- `llama3.1:8b` (higher quality, 6GB RAM)
- `mistral:7b` (alternative, 4GB RAM)

#### Selecting LLM Provider
Set via environment variable:
```bash
# Use Groq (fast cloud)
export GROQ_API_KEY="your_key"

# Force Ollama (local) even if Groq key exists
# Edit your profile and set use_groq=False in __init__
```

## Profile System

### Profile Structure
Each profile represents a specific user in a specific role:
- **User Directory**: `profiles/[username]/`
- **Role File**: `[role_name].py` containing experience and background
- **Job Description**: `[role_name]_job_description.txt` with target role requirements

### Creating Profiles
1. Copy template from `profiles/template/`
2. Customize personal information and experience
3. Add corresponding job description file
4. Ensure profile has `make_llm()` function

See [profiles/README.md](profiles/README.md) for complete setup guide.

## Job Description Integration

### Priority Order
1. `profiles/[user]/[role]_job_description.txt` (role-specific)
2. `profiles/[user]/job_descriptions/[role].txt` (organized folder)
3. `job_descriptions/[role].txt` (global by role)
4. `job_description.txt` (global fallback)

### Best Practices
- Include specific technical requirements
- List key responsibilities and skills
- Mention company context and values
- Keep concise but comprehensive (500-1000 words)

## Advanced Features

### Response Customization
Profiles support sophisticated prompt engineering:
- Experience-based response grounding
- Question-type specific instructions
- Technical depth adjustment
- STAR method formatting

### Error Handling
- Comprehensive fallback responses
- Audio device failure recovery
- LLM connection error handling
- Graceful degradation modes

### Performance Optimization
- Streaming response generation
- Real-time word wrapping
- Audio buffer management
- Memory-efficient processing

## Troubleshooting

### Common Issues

#### Audio Problems
**No audio captured**:
- Check audio device selection
- Verify microphone permissions
- Test with different audio devices
- Review system audio settings

**System audio not working**:
- Install virtual audio cable
- Configure WASAPI loopback (Windows)
- Setup PulseAudio monitors (Linux)
- Use BlackHole (macOS)

#### LLM Issues

**Groq API errors**:
```bash
# Check API key is set
echo $GROQ_API_KEY  # Should show your key

# Test Groq connection
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models

# If Groq fails, system auto-falls back to Ollama
```

**Ollama - Model not loading**:
```bash
# Check Ollama status
ollama list

# Pull model if missing
ollama pull llama3.2:3b

# Verify Ollama service
curl http://localhost:11434/api/tags
```

**Out of memory errors**:
- **With Groq**: No memory issues (cloud-based)
- **With Ollama**: Use smaller model (llama3.2:3b vs llama3.1:8b)
- Close other applications
- Check available RAM
- Reduce context window in profile

#### Profile Issues
**Profile not found**:
- Verify file path and naming
- Check `make_llm()` function exists
- Validate Python syntax
- Review profile structure

### System Requirements

#### Minimum
- 4GB RAM (with Groq)
- 8GB RAM (with Ollama)
- 2GB free disk space
- Python 3.8+
- Audio input device
- Internet connection (for Groq) or none needed (for Ollama)

#### Recommended
- 8GB RAM (Groq) or 16GB RAM (Ollama with large models)
- 5GB free disk space
- Python 3.10+
- Dedicated microphone or virtual audio setup
- Stable internet (for Groq)

## Development

### Contributing
1. Fork the repository
2. Create feature branch
3. Follow existing code style
4. Add comprehensive tests
5. Update documentation
6. Submit pull request

### Code Structure
- `main.py`: Application entry point and interview loop
- `src/core/`: Generic, reusable components
- `profiles/`: User-specific configurations
- Focus on modularity and maintainability

### Testing
```bash
# Run basic setup test
python test_setup.py

# Test audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test Groq connection (if using Groq)
python -c "from src.core.unified_llm_client import UnifiedLLMClient; c = UnifiedLLMClient('llama3.2:3b'); print('Provider:', c.get_provider())"

# Test Ollama connection (if using Ollama)
python -c "from src.core.ollama_client import OllamaClient; print(OllamaClient('llama3.2:3b').is_working())"
```

## License

MIT License - see LICENSE file for details.

## Support

### Documentation
- [Profile Setup Guide](profiles/README.md)
- [Audio Configuration Guide](docs/audio-setup.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

### Community
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and community support

### Technical Support
For technical issues:
1. Check troubleshooting section
2. Review system requirements
3. Test individual components
4. Create detailed issue report

---

## Recent Updates (November 2025)

### ✨ New Features
- **Dual LLM Support**: Groq API (cloud, fast) with automatic Ollama fallback (local, private)
- **Unified LLM Client**: Single interface for both Groq and Ollama with intelligent routing
- **Whisper Large Model**: Improved transcription accuracy with larger model
- **Enhanced Profile System**: Support for Groq in profile configuration

### 🔧 Improvements
- Faster response generation with Groq API (sub-second first token)
- Better error handling and fallback mechanisms
- Cleaner codebase with removed experimental features
- Updated documentation for dual LLM setup

### 🐛 Bug Fixes
- Fixed audio device detection reliability
- Improved stream handling for both LLM providers
- Better error messages for connection issues

---

**Note**: This system processes audio and personal information **locally by default** when using Ollama. When using Groq, data is sent to Groq's API for inference. Choose based on your privacy requirements.