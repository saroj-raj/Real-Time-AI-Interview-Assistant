# Real-Time AI Interview Assistant

A comprehensive AI-powered interview practice system that provides personalized, context-aware responses based on your professional background and target roles. Features real-time audio capture, transcription, and streaming LLM responses optimized for technical interviews.

## Features

### Core Capabilities
- **Real-time Audio Processing**: Manual start/stop recording with Whisper transcription
- **Profile-Based Responses**: Personalized answers based on your experience and target role
- **Streaming LLM Integration**: Local Ollama inference with real-time word wrapping
- **Job Description Alignment**: Responses tailored to specific job requirements
- **Multi-User Support**: Individual profiles for different users and roles
- **Cross-Platform Audio**: Windows WASAPI loopback and virtual audio device support

### Technical Features
- **Modular Architecture**: Clean separation between core components and user profiles
- **Audio Device Detection**: Automatic system audio and virtual device detection
- **Response Interruption**: Space key to stop LLM generation mid-response
- **Session Management**: Question numbering and interview flow control
- **Error Handling**: Comprehensive fallback mechanisms and error recovery

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
- **Audio**: OpenAI Whisper for transcription, sounddevice for capture
- **LLM**: Ollama for local inference (privacy-focused)
- **Language**: Python 3.8+ with minimal dependencies
- **Architecture**: Streaming responses with real-time processing

## Installation

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running
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

### Step 4: Install and Setup Ollama
```bash
# Install Ollama from https://ollama.com
# Pull a recommended model
ollama pull codellama:7b-instruct-q4_0
```

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

#### Supported Models
- `codellama:7b-instruct-q4_0` (recommended, 4GB RAM)
- `mistral:7b` (alternative, 4GB RAM)
- `llama3.1:8b` (higher quality, 6GB RAM)

#### Model Selection
Set via environment variable:
```bash
export OLLAMA_MODEL="codellama:7b-instruct-q4_0"
```

Or modify in profile file:
```python
# In your profile
self.model = "mistral:7b"
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
**Model not loading**:
```bash
# Check Ollama status
ollama list

# Pull model if missing
ollama pull codellama:7b-instruct-q4_0

# Verify Ollama service
curl http://localhost:11434/api/tags
```

**Out of memory errors**:
- Use smaller model (codellama:7b vs llama3.1:8b)
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
- 4GB RAM
- 2GB free disk space
- Python 3.8+
- Audio input device

#### Recommended
- 8GB RAM
- 5GB free disk space
- Python 3.10+
- Dedicated microphone or virtual audio setup

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

# Test Ollama connection
python -c "from src.core.ollama_client import OllamaClient; print(OllamaClient('codellama:7b-instruct-q4_0').is_working())"
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

**Note**: This system processes audio and personal information locally. No data is transmitted to external servers when using local Ollama models.