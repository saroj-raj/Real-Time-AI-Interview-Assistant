# Profile Setup Guide

This guide explains how to create and configure user profiles for the Real-Time AI Interview Assistant. Each profile represents a specific person preparing for a specific role.

## Overview

### Profile Structure
```
profiles/
├── README.md                    # This file
├── template/                    # Template files for creating new profiles
│   ├── example_role.py         # Example profile implementation
│   └── example_job_description.txt
└── [username]/                 # Your personal profile directory
    ├── role1.py               # Profile for Role 1
    ├── role1_job_description.txt
    ├── role2.py               # Profile for Role 2
    └── role2_job_description.txt
```

### Key Concepts
- **User**: Individual person (e.g., "john", "sarah", "alex")
- **Role**: Specific position being targeted (e.g., "senior_software_engineer", "data_scientist")
- **Profile**: Python file containing personal background and experience
- **Job Description**: Text file with target role requirements

## Quick Setup

### Step 1: Create Your User Directory
```bash
mkdir profiles/your_name
cd profiles/your_name
```

### Step 2: Copy Template Files
```bash
cp ../template/example_role.py your_role.py
cp ../template/example_job_description.txt your_role_job_description.txt
```

### Step 3: Customize Your Profile
Edit `your_role.py` with your actual experience and background.

### Step 4: Add Job Description
Edit `your_role_job_description.txt` with the target role requirements.

### Step 5: Test Your Profile
```bash
python -c "from profiles.your_name.your_role import make_llm; print('Profile works!')"
```

## Profile File Structure

### Required Components

Every profile file must include:

```python
import os, sys
from typing import Dict, List

# Add src/core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'core'))
from ollama_client import OllamaClient

class InterviewProfile:
    def __init__(self, model: str = None):
        # Personal Information (REQUIRED)
        self.name = "Your Full Name"
        self.role = "Target Role Title"
        self.experience_years = X
        
        # Technical Background (CUSTOMIZE)
        self.technical_skills = [...]
        self.work_experience = [...]
        self.achievements = [...]
        
        # LLM Setup (REQUIRED)
        self.model = model or "codellama:7b-instruct-q4_0"
        self.llm = OllamaClient(self.model)

    def generate_stream(self, question: str, context: str = "", job_description: str = ""):
        """Required method for streaming responses"""
        return self.generate_response_stream(question, context, job_description)

    def generate_response_stream(self, question: str, context: str = "", job_description: str = ""):
        """Generate streaming interview responses"""
        prompt = self._build_interview_prompt(question, context, job_description)
        fallback = self._get_comprehensive_fallback(question)
        
        options = {
            "temperature": 0.3,
            "num_ctx": 4096,
            "num_predict": 800,
            "top_p": 0.9,
        }
        
        yield from self.llm.generate_stream(prompt, options, fallback)

    # Additional methods for prompt building and fallbacks...

def make_llm():
    """Required factory function"""
    return InterviewProfile()
```

### Personal Information Fields

```python
# Basic Details
self.name = "Your Full Name"
self.role = "Target Role (e.g., Senior Software Engineer)"
self.experience_years = 5
self.phone = "+1 (555) 123-4567"  # Optional
self.email = "your.email@example.com"  # Optional
self.linkedin = "linkedin.com/in/yourprofile"  # Optional
self.github = "github.com/yourusername"  # Optional

# Education
self.education = "Degree, University, Year"
```

### Technical Skills Structure

```python
# Programming Languages
self.programming_languages = [
    "Python (NumPy, Pandas, Django)",
    "JavaScript (React, Node.js)",
    "Java, C++, SQL"
]

# Frameworks and Tools
self.frameworks = [
    "TensorFlow, PyTorch, Scikit-learn",
    "React, Angular, Vue.js",
    "Docker, Kubernetes, AWS"
]

# Databases
self.databases = [
    "PostgreSQL, MySQL, MongoDB",
    "Redis, Elasticsearch"
]

# Cloud Platforms
self.cloud_platforms = [
    "AWS (EC2, S3, Lambda, RDS)",
    "GCP (Compute Engine, Cloud Storage)",
    "Azure (VMs, Blob Storage)"
]
```

### Work Experience Structure

```python
self.work_experience = [
    {
        "role": "Senior Software Engineer",
        "company": "Tech Company Inc.",
        "location": "San Francisco, CA",
        "duration": "Jan 2022 - Present",
        "key_projects": [
            "Led development of microservices architecture serving 1M+ users",
            "Implemented CI/CD pipeline reducing deployment time by 60%",
            "Mentored 3 junior developers on best practices and code review"
        ]
    },
    {
        "role": "Software Engineer",
        "company": "Startup LLC",
        "location": "New York, NY", 
        "duration": "Jun 2020 - Dec 2021",
        "key_projects": [
            "Built REST API handling 10K+ requests per minute",
            "Developed React frontend with 99.9% uptime",
            "Optimized database queries improving performance by 40%"
        ]
    }
]
```

### Achievements with Metrics

```python
self.achievements = [
    "Reduced system latency from 500ms to 50ms through optimization",
    "Increased test coverage from 60% to 95% across core services",
    "Led migration to cloud infrastructure saving $50K annually",
    "Implemented monitoring system reducing incident response time by 70%"
]
```

## Job Description Files

### Naming Convention
- `[role_name]_job_description.txt`
- Example: `senior_software_engineer_job_description.txt`

### Content Structure
```
About the Role
We are seeking a Senior Software Engineer to join our team...

Key Responsibilities
- Design and implement scalable web applications
- Collaborate with cross-functional teams
- Mentor junior developers

Required Skills
- 5+ years of software development experience
- Proficiency in Python, JavaScript, and SQL
- Experience with cloud platforms (AWS/GCP/Azure)
- Strong problem-solving and communication skills

Preferred Qualifications
- Experience with microservices architecture
- Knowledge of containerization (Docker/Kubernetes)
- Previous experience in fintech or e-commerce

Company Culture
We value innovation, collaboration, and continuous learning...
```

### Best Practices for Job Descriptions
- Include specific technical requirements
- Mention company values and culture
- Add context about team size and structure
- Keep between 500-1000 words
- Focus on most important requirements first

## Advanced Customization

### Response Customization

#### Question-Specific Instructions
```python
def _get_detailed_question_instructions(self, question: str) -> str:
    q_lower = question.lower()
    
    if any(phrase in q_lower for phrase in ["tell me about yourself", "introduce"]):
        return (
            "Provide a comprehensive professional summary covering:\n"
            "- Your current role and years of experience\n"
            "- Key technical skills and expertise areas\n"
            "- Recent significant achievements\n"
            "- What excites you about this opportunity\n"
        )
    elif any(phrase in q_lower for phrase in ["technical challenge", "difficult problem"]):
        return (
            "Use the STAR method:\n"
            "- Situation: Context and background\n"
            "- Task: What you needed to accomplish\n"
            "- Action: Specific steps you took\n"
            "- Result: Quantified outcome and impact\n"
        )
    # Add more question types...
```

#### Fallback Response Customization
```python
def _get_comprehensive_fallback(self, question: str) -> str:
    q_lower = question.lower()
    
    if any(phrase in q_lower for phrase in ["experience", "background"]):
        return (
            f"I'm {self.name}, a {self.role} with {self.experience_years} years "
            f"of experience. In my current role at [Company], I focus on [key areas]. "
            f"One achievement I'm proud of is [specific example with metrics]."
        )
    # Add more fallback patterns...
```

### Model Configuration

#### Model Selection
```python
# Choose based on your hardware
preferred_models = [
    "codellama:7b-instruct-q4_0",  # 4GB RAM, good for coding interviews
    "mistral:7b-instruct",         # 4GB RAM, general purpose
    "llama3.1:8b-instruct",        # 6GB RAM, higher quality
]

self.model = model or os.environ.get("OLLAMA_MODEL", preferred_models[0])
```

#### Generation Parameters
```python
options = {
    "temperature": 0.3,      # Lower for more consistent responses
    "num_ctx": 4096,         # Context window size
    "num_predict": 800,      # Maximum response length
    "top_p": 0.9,           # Nucleus sampling
    "stop": ["\\nHuman:", "\\nInterviewer:"]  # Stop sequences
}
```

## Testing Your Profile

### Basic Validation
```python
# Test profile loading
from profiles.your_name.your_role import make_llm
profile = make_llm()
print(f"Profile loaded: {profile.name}")

# Test response generation
response = ""
for token in profile.generate_stream("Tell me about yourself."):
    response += token
print(f"Response: {response}")
```

### Common Issues

#### Import Errors
```python
# Ensure correct path setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'core'))
```

#### Missing Methods
```python
# Required methods
def generate_stream(self, question, context="", job_description=""):
    return self.generate_response_stream(question, context, job_description)

def make_llm():  # At module level
    return InterviewProfile()
```

#### Model Loading Issues
```bash
# Check available models
ollama list

# Pull required model
ollama pull codellama:7b-instruct-q4_0
```

## Profile Templates

### Software Engineer Template
```python
class InterviewProfile:
    def __init__(self, model: str = None):
        # Customize these fields
        self.name = "John Smith"
        self.role = "Senior Software Engineer"
        self.experience_years = 5
        
        self.programming_languages = [
            "Python (Django, Flask, FastAPI)",
            "JavaScript (React, Node.js, TypeScript)",
            "Java, Go, SQL"
        ]
        
        self.work_experience = [
            {
                "role": "Software Engineer",
                "company": "Tech Startup",
                "duration": "2020-Present",
                "key_projects": [
                    "Built microservices architecture serving 1M users",
                    "Implemented CI/CD pipeline with 99.9% uptime"
                ]
            }
        ]
        # ... rest of implementation
```

### Data Scientist Template
```python
class InterviewProfile:
    def __init__(self, model: str = None):
        self.name = "Jane Doe"
        self.role = "Senior Data Scientist"
        self.experience_years = 4
        
        self.technical_skills = [
            "Python (Pandas, NumPy, Scikit-learn)",
            "R, SQL, Spark",
            "TensorFlow, PyTorch, Keras"
        ]
        
        self.ml_expertise = [
            "Deep Learning, NLP, Computer Vision",
            "Statistical Modeling, A/B Testing",
            "MLOps, Model Deployment, Monitoring"
        ]
        # ... rest of implementation
```

## Security and Privacy

### Personal Information
- Keep sensitive information out of version control
- Use placeholder values in templates
- Consider using environment variables for sensitive data

### Best Practices
- Don't commit actual personal profiles to public repositories
- Use generic examples in documentation
- Test with sample data before using real information

## Troubleshooting

### Profile Not Loading
1. Check file naming convention
2. Verify `make_llm()` function exists
3. Ensure proper imports
4. Test Python syntax

### Response Quality Issues
1. Add more specific experience details
2. Customize fallback responses
3. Adjust generation parameters
4. Include relevant job description

### Performance Issues
1. Use smaller model if needed
2. Reduce context window size
3. Lower `num_predict` parameter
4. Check available system memory

## Support

For additional help:
1. Review main project README.md
2. Check example templates
3. Test individual components
4. Create GitHub issue with specific error details

---

**Remember**: Profiles contain personal information. Keep them private and never commit real personal data to public repositories.