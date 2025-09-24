# Real-Time AI Interview Assistant

A sophisticated AI-powered interview assistant that provides real-time responses to technical interview questions. Built specifically for Agentic AI Engineer positions with comprehensive LLM evaluation expertise.

## Features

- **Real-Time Audio Processing**: Captures system audio or microphone input
- **Speech-to-Text**: Uses Whisper for accurate transcription
- **Intelligent Response Generation**: Leverages Ollama LLMs for contextual interview responses
- **Modular Architecture**: Separates generic LLM client from personal profile data
- **Comprehensive Technical Knowledge**: Covers Agentic AI, LLM evaluation, RAG systems, and more
- **Production-Ready**: Handles errors gracefully with intelligent fallbacks

## Architecture

```
├── main.py                 # Main application entry point
├── ollama_client.py        # Generic Ollama LLM client
├── interview_profile.py    # Personal background and responses
├── llm_client.py           # Integration layer (backward compatibility)
├── audio_device_util.py    # Audio device detection and management
├── audio_transcriber.py    # Whisper integration for speech-to-text
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Prerequisites

### 1. Ollama Installation

Install Ollama on your system:

**Windows/Mac/Linux:**
```bash
# Download from https://ollama.ai/
curl -fsSL https://ollama.ai/install.sh | sh
```

**Pull a recommended model:**
```bash
# Best for memory-constrained systems (3.8GB)
ollama pull codellama:7b-instruct-q4_0

# Alternative models
ollama pull mistral:7b          # 4.4GB
ollama pull llama3.1:8b         # 4.9GB (requires ~6GB RAM)
```

### 2. Audio Setup

**Option A: WASAPI Loopback (Recommended for Windows)**
- Automatically captures system audio from speakers/headphones
- No additional setup required

**Option B: Virtual Audio Cable**
- Download VB-Audio CABLE or Voicemeeter
- Route interview audio through virtual device

**Option C: Physical Microphone**
- Use built-in microphone to pick up audio from speakers
- Less reliable but works as fallback

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Real-TimeAIInterviewAssistant
```

2. **Create virtual environment:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify Ollama is running:**
```bash
ollama serve  # If not already running
ollama list   # Check available models
```

## Configuration

### Environment Variables (Optional)

```bash
# Set preferred model
export OLLAMA_MODEL="codellama:7b-instruct-q4_0"

# Set Ollama URL (if running on different host)
export OLLAMA_URL="http://localhost:11434"

# Force specific audio device
export FORCE_DEVICE_INDEX="5"

# Custom context file
export CONTEXT_FILE="my_custom_context.txt"

# Custom job description file
export JOB_DESCRIPTION_FILE="my_job_description.txt"
```

### Context Files (Optional)

Create these files to provide additional context:

**my_context.txt** - Additional personal background
```
Additional technical experience, projects, or context
that should be included in responses...
```

**job_description.txt** - Target job description
```
Paste the job description you're interviewing for
to get more targeted responses...
```

## Usage

### Basic Usage

1. **Start the application:**
```bash
python main.py
```

2. **Follow the initialization:**
```
AI Interview Assistant - Initializing...
============================================================
✓ Context: 150 words loaded
✓ Job Description: 200 words loaded

--- Audio Setup ---
Device: Speakers (Realtek Audio)
Mode: WASAPI speaker loopback
Rate: 48000Hz

--- Model Loading ---
Loading Whisper... ✓
Loading LLM... ✓

READY FOR INTERVIEW
============================================================
Controls:
• Press ENTER to START recording
• Press ENTER again to STOP recording  
• Press SPACE during AI response to interrupt
• Press CTRL+C to exit
============================================================
```

3. **During interview:**
   - Press ENTER to start recording a question
   - Press ENTER again to stop recording
   - Wait for transcription and AI response
   - Press SPACE to interrupt long responses
   - Continue for next question

### Advanced Usage

**Test specific model:**
```bash
OLLAMA_MODEL="mistral:7b" python main.py
```

**Debug audio devices:**
```bash
python audio_device_util.py
```

**Test LLM connection:**
```bash
python llm_client.py
```

## Supported Interview Topics

The assistant is trained on comprehensive technical knowledge including:

### Agentic AI & Multi-Agent Systems
- LangChain, CrewAI, LangGraph, AutoGen frameworks
- Planner-Executor patterns and goal-oriented agents
- Tool-augmented reasoning and contextual memory
- Multi-agent orchestration and collaboration

### LLM Evaluation & Scoring  
- RAGAS framework implementation
- Faithfulness, Answer Relevancy, Context Precision metrics
- A/B testing and benchmark scoring
- Custom evaluation pipelines

### Retrieval-Augmented Generation (RAG)
- Vector databases: Pinecone, Weaviate, Milvus, FAISS
- Embedding optimization and semantic search
- Multi-modal RAG for text, PDFs, images
- Context windowing and chunk strategies

### Production ML & MLOps
- Cloud platforms: AWS SageMaker, Azure OpenAI, GCP Vertex AI
- Containerization with Docker and Kubernetes
- CI/CD pipelines and monitoring
- Model serving and scaling strategies

### Large Language Models
- Fine-tuning with domain-specific datasets
- Prompt engineering (few-shot, CoT, ReAct)
- LLM deployment and optimization
- Multi-modal model integration

## Customization

### Personal Profile Modification

Edit `interview_profile.py` to customize:

```python
# Personal Information
self.name = "Your Name"
self.role = "Your Role"
self.experience_years = 5

# Technical Expertise
self.agentic_ai_expertise = [
    "Your specific frameworks and tools",
    # ... add your expertise
]

# Work Experience
self.work_experience = [
    {
        "role": "Your Role",
        "company": "Your Company", 
        "duration": "Start - End",
        "key_projects": ["Your achievements"]
    }
]
```

### Model Selection

The system automatically selects the best available model based on your memory:

1. **codellama:7b-instruct-q4_0** (3.8GB) - Recommended for most systems
2. **mistral:7b** (4.4GB) - Good alternative
3. **llama3.1:8b** (4.9GB) - Best quality, requires more memory

### Response Customization

Modify fallback responses in `interview_profile.py`:

```python
def _get_comprehensive_fallback(self, question: str) -> str:
    # Customize responses based on question type
    if "your_specific_topic" in question.lower():
        return "Your customized response..."
```

## Troubleshooting

### Common Issues

**1. "Model requires more system memory" error**
```bash
# Use smaller model
export OLLAMA_MODEL="codellama:7b-instruct-q4_0"
```

**2. Audio device not detected**
```bash
# List all devices
python audio_device_util.py

# Force specific device
export FORCE_DEVICE_INDEX="3"
```

**3. Ollama connection failed**
```bash
# Check if Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

**4. Poor transcription quality**
- Increase audio volume
- Reduce background noise
- Use headphones instead of speakers
- Check microphone placement

**5. Generic fallback responses**
- Ensure Ollama model is loaded: `ollama list`
- Check memory usage
- Try smaller model
- Verify network connection to Ollama

### Performance Optimization

**For better response speed:**
```python
# In interview_profile.py, reduce context size
"num_ctx": 2048,  # Reduce from 4096
"num_predict": 400,  # Reduce from 800
```

**For better accuracy:**
```python
# Use larger model if memory allows
export OLLAMA_MODEL="llama3.1:8b"
```

## System Requirements

- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 5GB free space for models
- **CPU**: Modern multi-core processor
- **Audio**: Microphone or system audio access
- **OS**: Windows 10+, macOS 10.14+, or Linux

## Model Recommendations by System

| RAM Available | Recommended Model | Performance |
|---------------|------------------|-------------|
| 4-6 GB | codellama:7b-instruct-q4_0 | Good |
| 6-8 GB | mistral:7b | Better |
| 8+ GB | llama3.1:8b | Best |

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Ollama** for local LLM inference
- **OpenAI Whisper** for speech-to-text
- **Hugging Face** for model ecosystem
- **LangChain** framework inspiration for agent patterns

## Contact

For questions or support, please open an issue in the repository.