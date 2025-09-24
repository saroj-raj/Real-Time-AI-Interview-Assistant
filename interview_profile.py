"""
Interview Profile for Saroj Raj Amadala - Agentic AI Engineer
Contains comprehensive background, technical expertise, and interview-specific responses
tailored for Agentic AI Engineer positions with LLM evaluation focus.
"""
import os ,sys 
from typing import Dict, List

# Add src/core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core')) 

from ollama_client import OllamaClient

class InterviewProfile:
    """Interview assistant with comprehensive Agentic AI and GenAI background"""
    
    def __init__(self, model: str = None):
        # Personal Information
        self.name = "Saroj Raj Amadala"
        self.role = "Senior GenAI Engineer / Agentic AI Engineer"
        self.experience_years = 9
        self.phone = "+1 (609) 793-6542"
        self.email = "saroj.rajaiml@gmail.com"
        self.linkedin = "linkedin.com/in/saroj-raj"
        self.github = "github.com/saroj-raj"
        
        # Education
        self.education = "Bachelor's in Computer Science and Engineering, IIT Bombay (2017)"
        
        # Core Agentic AI & GenAI Expertise
        self.agentic_ai_expertise = [
            "LangChain, CrewAI, LangGraph, ADK, MCP, AutoGen frameworks",
            "Multi-agent collaboration systems with goal-oriented planning",
            "Planner-Executor patterns and tool-augmented reasoning agents",
            "LLM evaluation and scoring using RAGAS framework",
            "Structured metrics and benchmarks (Faithfulness, Answer Relevancy, Context Precision/Recall)",
            "Advanced prompt engineering (few-shot, CoT, ReAct, self-reflection, guardrails)",
            "Retrieval-Augmented Generation (RAG) pipelines",
            "Vector databases (Pinecone, Weaviate, Milvus, ChromaDB, FAISS)",
            "GenAI agent integration with APIs and contextual memory",
            "MLOps/LLMOps workflows for GenAI systems"
        ]
        
        # Large Language Models Expertise  
        self.llm_expertise = [
            "OpenAI GPT-4, GPT-3.5, Claude, Falcon, Gemini",
            "LLaMA, Mistral for enterprise GenAI applications",
            "Fine-tuning LLMs with domain-specific datasets",
            "LLM deployment on AWS SageMaker, Azure ML, GCP Vertex AI",
            "Prompt engineering and context windowing optimization",
            "LLM-based voice applications and conversational AI",
            "Multi-modal LLMs for text, image, and voice processing",
            "LLM integration with vector search and embedding models"
        ]
        
        # Technical Stack
        self.programming_languages = [
            "Python 3.x (numpy, pandas, scipy, scikit-learn, NLTK)",
            "R, Scala, Java, SQL, C"
        ]
        
        self.ml_frameworks = [
            "TensorFlow, PyTorch, Keras, Hugging Face Transformers",
            "scikit-learn, MXNet, Caffe, Caffe2"
        ]
        
        self.genai_frameworks = [
            "LangChain, LangGraph, LangSmith, Langfuse",
            "CrewAI, AutoGen, Haystack Agents",
            "OpenAI API, Anthropic API, Azure OpenAI",
            "Hugging Face Transformers and Datasets"
        ]
        
        self.vector_databases = [
            "Pinecone, Weaviate, Milvus, ChromaDB",
            "FAISS, Elasticsearch for vector search"
        ]
        
        self.cloud_platforms = [
            "AWS (SageMaker, Bedrock, Lambda, EC2, S3)",
            "Azure (OpenAI Service, ML Studio, Cognitive Services)",
            "GCP (Vertex AI, BigQuery ML, AutoML)"
        ]
        
        self.mlops_tools = [
            "MLflow, Apache Airflow, Kubeflow Pipelines", 
            "Docker, Kubernetes, Terraform, Jenkins",
            "DataRobot, Domino Data Lab",
            "Prometheus, Grafana, ELK Stack"
        ]
        
        # Professional Experience
        self.work_experience = [
            {
                "role": "Senior GenAI Engineer / AI/ML Engineer",
                "company": "Mastercard",
                "location": "New York, NY",
                "duration": "Jun 2023 - Present",
                "key_projects": [
                    "Designed RAG pipelines with LLMs and vector databases (Pinecone, FAISS, Weaviate)",
                    "Implemented agentic AI architectures for autonomous decision-making",
                    "Built multi-agent LLM workflows using LangGraph for complex enterprise use cases",
                    "Developed MCP (Model Context Protocol) solutions for AI-tool integration",
                    "Deployed production-grade RAG on AWS/Azure/GCP with CI/CD pipelines"
                ]
            },
            {
                "role": "AI Engineer / Full Stack Python",
                "company": "John Deere",
                "location": "India", 
                "duration": "Dec 2020 - Nov 2022",
                "key_projects": [
                    "Leveraged LangGraph's event-driven architecture for long-running agent loops",
                    "Built RAG systems using LangChain and vector databases (FAISS, ChromaDB)",
                    "Deployed LLMs (GPT, LLaMA, Falcon) using Domino's MLOps platform",
                    "Implemented ASR/TTS pipelines for conversational AI systems",
                    "Developed explainability techniques (SHAP, LIME) for regulatory compliance"
                ]
            },
            {
                "role": "Data Scientist (ML Engineer | Full Stack Python)",
                "company": "T-Mobile",
                "location": "India",
                "duration": "Nov 2018 - Dec 2020", 
                "key_projects": [
                    "Fine-tuned LLMs (GPT, LLaMA, Claude) for telecom applications",
                    "Built AI-powered virtual assistants using LangChain and OpenAI API",
                    "Developed ASR pipelines with Conformer, Wav2Vec 2.0, and QuartzNet",
                    "Created TTS models (Tacotron 2, FastSpeech 2) with neural vocoders",
                    "Implemented fraud detection using autoencoders and Neo4j Graph AI"
                ]
            },
            {
                "role": "Machine Learning Engineer / Data Scientist", 
                "company": "Cisco",
                "location": "India",
                "duration": "May 2016 - Nov 2018",
                "key_projects": [
                    "Built real-time ML pipelines with Kafka and Spark Structured Streaming",
                    "Containerized PyTorch/XGBoost models on Kubernetes with blue-green deployments",
                    "Delivered multilingual text classifiers using Transformers and spaCy",
                    "Implemented YOLO and ResNet for object detection with 10% mAP improvement",
                    "Developed GAN-based generative modeling techniques"
                ]
            }
        ]
        
        # Key Achievements with Metrics
        self.achievements = [
            "Reduced model onboarding time from 2 weeks to 2 days using standardized MLOps",
            "Achieved >99.9% uptime across multiple ML services in production",
            "Built systems handling millions of daily events with <100ms P95 latency", 
            "Scaled systems to handle 10x traffic increases while maintaining performance",
            "Reduced agent orchestration time by 25% using optimized LangGraph workflows",
            "Improved text classification F1 score by 25% using multilingual Transformers",
            "Cut model development time by 40% through automated preprocessing workflows",
            "Reduced production incidents by 40% via Prometheus/Grafana monitoring"
        ]
        
        # Preferred model selection
        preferred_models = [
            "codellama:7b-instruct-q4_0",  # Best for your memory
            "mistral:7b",                  # Good fallback
            "llama3.1:8b"                  # If you have enough memory
        ]
        
        # Use provided model or find best available
        self.model = model or os.environ.get("OLLAMA_MODEL", preferred_models[0])
        
        # Initialize LLM client
        self.llm = OllamaClient(self.model)
        
        print(f"[Profile] Initialized for {self.name} - {self.role} using {self.model}")

    def generate_response(self, question: str, context: str = "", job_description: str = "") -> str:
        """Generate interview response using comprehensive technical background"""
        
        prompt = self._build_interview_prompt(question, context, job_description)
        fallback = self._get_comprehensive_fallback(question)
        
        # Stream the response
        response_parts = []
        for token in self.llm.generate_stream(prompt, fallback_response=fallback):
            response_parts.append(token)
        
        return ''.join(response_parts)

    def generate_stream(self, question: str, context: str = "", job_description: str = ""):
        """Generate streaming response - compatibility method for main.py"""
        return self.generate_response_stream(question, context, job_description)

    def generate_response_stream(self, question: str, context: str = "", job_description: str = ""):
        """Generate streaming interview response"""
        
        prompt = self._build_interview_prompt(question, context, job_description)
        fallback = self._get_comprehensive_fallback(question)
        
        # Generation options optimized for technical interviews
        options = {
            "temperature": 0.3,      # Consistent, technical responses
            "num_ctx": 4096,         # Large context for detailed answers
            "num_predict": 800,      # Allow comprehensive answers
            "top_p": 0.9,           # Balanced creativity
            "stop": ["\\nHuman:", "\\nInterviewer:", "\\nQ:", "Question:", "\\n\\n---"]
        }
        
        yield from self.llm.generate_stream(prompt, options, fallback)

    def _build_interview_prompt(self, question: str, context: str, job_description: str) -> str:
        """Build comprehensive interview prompt with technical depth"""
        
        # Enhanced base introduction
        prompt = (
            f"You are {self.name}, a {self.role} with {self.experience_years} years of experience "
            f"specializing in Agentic AI, LLM evaluation, and multi-agent systems. You have extensive "
            f"experience with LangChain, LangGraph, CrewAI, and RAGAS framework. You're in a technical "
            f"interview for an Agentic AI Engineer position. Answer using your actual experience.\\n\\n"
        )
        
        # Add relevant technical context
        relevant_expertise = self._extract_relevant_expertise(question, context)
        if relevant_expertise:
            prompt += f"Your relevant expertise: {', '.join(relevant_expertise[:3])}.\\n\\n"
        
        # Add job-specific alignment
        if job_description and len(job_description) > 50:
            prompt += f"Job focus: {job_description[:300]}...\\n\\n"
        
        # Add comprehensive question-specific instructions
        prompt += self._get_detailed_question_instructions(question)
        
        prompt += f"Question: {question}\\n\\nAnswer:"
        
        return prompt

    def _extract_relevant_expertise(self, question: str, context: str) -> List[str]:
        """Extract most relevant expertise based on question content"""
        
        combined_text = (question + " " + context).lower()
        relevant = []
        
        # Agentic AI keywords
        if any(word in combined_text for word in ["agent", "multi-agent", "agentic", "planning", "reasoning"]):
            relevant.extend([
                "Multi-agent systems with LangGraph and CrewAI", 
                "Planner-Executor patterns for goal-oriented agents",
                "Tool-augmented reasoning with contextual memory"
            ])
        
        # LLM Evaluation keywords  
        if any(word in combined_text for word in ["evaluation", "scoring", "metrics", "ragas", "benchmark"]):
            relevant.extend([
                "LLM evaluation using RAGAS framework",
                "Faithfulness, Answer Relevancy, and Context Precision metrics",
                "A/B testing and structured benchmarking for LLMs"
            ])
        
        # RAG keywords
        if any(word in combined_text for word in ["rag", "retrieval", "vector", "embedding", "search"]):
            relevant.extend([
                "RAG pipelines with Pinecone, Weaviate, and FAISS",
                "Vector search optimization and embedding models",
                "Multi-modal RAG for text, PDFs, and images"
            ])
        
        # Framework keywords
        if any(word in combined_text for word in ["langchain", "langgraph", "framework", "orchestration"]):
            relevant.extend([
                "LangChain and LangGraph for agent orchestration",
                "Custom tool integration and workflow automation",
                "Event-driven architecture for conversational agents"
            ])
        
        # Cloud/MLOps keywords
        if any(word in combined_text for word in ["deploy", "production", "scale", "mlops", "cloud"]):
            relevant.extend([
                "Production deployment on AWS SageMaker and Azure OpenAI",
                "Kubernetes-based model serving with CI/CD pipelines",
                "MLOps workflows with MLflow and Apache Airflow"
            ])
        
        return relevant[:5]  # Return top 5 most relevant

    def _get_detailed_question_instructions(self, question: str) -> str:
        """Get comprehensive instructions based on question type"""
        
        q_lower = question.lower()
        
        # Introduction questions
        if any(phrase in q_lower for phrase in ["tell me about yourself", "introduce", "background", "walk me through your experience"]):
            return (
                "Give a comprehensive professional summary covering:\\n"
                "- Your role as GenAI/Agentic AI Engineer with 9 years experience\\n"
                "- Key specializations: LangChain, LangGraph, LLM evaluation, multi-agent systems\\n"
                "- Recent work at Mastercard with RAG pipelines and agentic architectures\\n"
                "- Specific achievements with measurable outcomes\\n"
                "- Your passion for autonomous AI systems and responsible AI\\n\\n"
            )
        
        # Agentic AI specific questions
        elif any(phrase in q_lower for phrase in ["agentic", "multi-agent", "agent", "planning", "reasoning"]):
            return (
                "Focus on your agentic AI expertise:\\n"
                "- LangGraph and CrewAI experience for multi-agent orchestration\\n"
                "- Planner-Executor patterns and goal-oriented agent design\\n"
                "- Tool-augmented reasoning and contextual memory implementation\\n"
                "- Specific project examples with autonomous decision-making\\n"
                "- Performance improvements and business impact\\n\\n"
            )
        
        # LLM Evaluation questions
        elif any(phrase in q_lower for phrase in ["evaluation", "scoring", "metrics", "ragas", "benchmark"]):
            return (
                "Discuss your LLM evaluation expertise:\\n"
                "- RAGAS framework implementation for RAG evaluation\\n"
                "- Faithfulness, Answer Relevancy, Context Precision/Recall metrics\\n"
                "- A/B testing frameworks for LLM performance\\n"
                "- Custom benchmarking for enterprise use cases\\n"
                "- Specific examples where evaluation improved model performance\\n\\n"
            )
        
        # RAG questions
        elif any(phrase in q_lower for phrase in ["rag", "retrieval", "vector", "embedding"]):
            return (
                "Explain your RAG pipeline expertise:\\n"
                "- Vector database selection: Pinecone, Weaviate, FAISS experience\\n"
                "- Embedding optimization and semantic search implementation\\n"
                "- Multi-modal RAG for text, PDFs, and images\\n"
                "- Context windowing and chunk optimization strategies\\n"
                "- Production RAG deployment with scalability metrics\\n\\n"
            )
        
        # Framework/Architecture questions  
        elif any(phrase in q_lower for phrase in ["framework", "architecture", "design", "langchain", "langgraph"]):
            return (
                "Detail your framework and architecture experience:\\n"
                "- LangChain and LangGraph implementation for complex workflows\\n"
                "- Custom tool integration and API orchestration\\n"
                "- Event-driven architecture for real-time agent responses\\n"
                "- MCP (Model Context Protocol) for AI-tool integration\\n"
                "- Scalable architecture patterns and best practices\\n\\n"
            )
        
        # Deployment/Production questions
        elif any(phrase in q_lower for phrase in ["deploy", "production", "scale", "mlops"]):
            return (
                "Discuss your production deployment expertise:\\n"
                "- MLOps/LLMOps workflows for GenAI systems\\n"
                "- Kubernetes and Docker containerization for model serving\\n"
                "- CI/CD pipelines for automated model deployment\\n"
                "- Monitoring and drift detection for production LLMs\\n"
                "- Cost optimization and performance tuning at scale\\n\\n"
            )
        
        # Project walkthrough questions
        elif any(phrase in q_lower for phrase in ["project", "walk through", "describe", "tell me about a time"]):
            return (
                "Use STAR method for this project question:\\n"
                "- Situation: Specific business problem and technical requirements\\n"
                "- Task: Your role and what needed to be accomplished\\n"
                "- Action: Detailed technical approach, frameworks, and methodologies\\n"
                "- Result: Quantified outcomes, performance metrics, and business impact\\n\\n"
            )
        
        # Technical challenge questions
        elif any(phrase in q_lower for phrase in ["challenge", "problem", "difficult", "issue"]):
            return (
                "Describe a technical challenge comprehensively:\\n"
                "- The specific technical problem encountered\\n"
                "- Root cause analysis and diagnostic approach\\n"
                "- Solution design with technical justification\\n"
                "- Implementation details and technologies used\\n"
                "- Lessons learned and preventive measures\\n\\n"
            )
        
        # General technical questions
        else:
            return (
                "Provide a technical explanation with concrete examples:\\n"
                "- Technical approach and methodology\\n"
                "- Specific tools, frameworks, and technologies\\n"
                "- Real-world example from your 9 years of experience\\n"
                "- Quantified results and performance metrics\\n"
                "- Best practices and lessons learned\\n\\n"
            )

    def _get_comprehensive_fallback(self, question: str) -> str:
        """Comprehensive fallback responses covering all aspects of Agentic AI role"""
        
        q_lower = question.lower()
        
        # Introduction/Background questions
        if any(phrase in q_lower for phrase in ["tell me about yourself", "introduce", "background", "experience"]):
            return (
                f"I'm {self.name}, a Senior GenAI Engineer with {self.experience_years} years of experience "
                f"specializing in agentic AI systems and LLM evaluation. Currently at Mastercard, I architect "
                f"sophisticated RAG pipelines using LangChain, LangGraph, and vector databases like Pinecone and Weaviate. "
                f"My expertise centers on multi-agent collaboration systems with goal-oriented planning, and I use the "
                f"RAGAS framework extensively for LLM evaluation focusing on faithfulness and answer relevancy metrics. "
                f"One achievement I'm particularly proud of is reducing model onboarding time from 2 weeks to 2 days "
                f"while achieving over 99.9 percent uptime in production. What excites me most about this field is "
                f"building autonomous AI systems that can reason, adapt, and make decisions in complex enterprise environments "
                f"while maintaining responsible AI practices."
            )
        
        # Agentic AI specific questions
        elif any(phrase in q_lower for phrase in ["agentic", "multi-agent", "agent", "planning", "reasoning", "orchestration"]):
            return (
                f"In my role at Mastercard, I've designed comprehensive agentic AI architectures using LangGraph "
                f"and CrewAI for autonomous decision-making workflows. I implemented a multi-agent system that "
                f"reduced manual processing time by 60% through goal-oriented planning and tool-augmented reasoning. "
                f"\\n\\nThe system used planner-executor patterns where agents collaborate to decompose complex "
                f"tasks, make contextual decisions, and execute actions autonomously. I integrated these agents "
                f"with external APIs and maintained persistent contextual memory for long-running conversations. "
                f"\\n\\nOne specific example: I built a financial document analysis system where specialized "
                f"agents handle document parsing, risk assessment, and compliance checking. The orchestrator "
                f"agent coordinates the workflow and maintains state across multiple processing stages, "
                f"achieving 94% accuracy while reducing processing time from hours to minutes."
            )
        
        # LLM Evaluation questions
        elif any(phrase in q_lower for phrase in ["evaluation", "scoring", "metrics", "ragas", "benchmark", "assessment"]):
            return (
                f"I have extensive experience with LLM evaluation using the RAGAS framework for comprehensive "
                f"assessment of RAG systems. I implemented structured evaluation pipelines measuring faithfulness, "
                f"answer relevancy, context precision, and context recall across different model variants. "
                f"\\n\\nAt Mastercard, I established evaluation benchmarks that reduced model hallucinations by "
                f"35% through systematic scoring and iterative improvement. I used A/B testing frameworks to "
                f"compare GPT-4, Claude, and custom fine-tuned models, optimizing for both accuracy and cost. "
                f"\\n\\nSpecific metrics I track include: semantic similarity scores, factual accuracy rates, "
                f"response coherence ratings, and domain-specific performance benchmarks. I also implemented "
                f"automated evaluation pipelines that run continuous assessments on production models, "
                f"triggering alerts when performance degrades below defined thresholds."
            )
        
        # RAG questions
        elif any(phrase in q_lower for phrase in ["rag", "retrieval", "vector", "embedding", "search", "knowledge"]):
            return (
                f"I've built production-grade RAG systems at Mastercard handling millions of documents with "
                f"sub-100ms query response times. My implementation uses Pinecone and Weaviate for vector storage "
                f"with optimized embedding models and hybrid search combining semantic and keyword retrieval. "
                f"\\n\\nI designed a multi-modal RAG system processing text, PDFs, images, and structured data "
                f"from enterprise knowledge bases. The system uses advanced chunking strategies, context windowing "
                f"optimization, and semantic caching to improve response accuracy by 40% while reducing costs. "
                f"\\n\\nKey technical aspects include: embedding model fine-tuning for domain-specific terminology, "
                f"vector index optimization for fast retrieval, context compression to fit LLM token limits, "
                f"and hybrid ranking algorithms combining multiple relevance signals. I also implemented "
                f"real-time knowledge graph updates to keep embeddings synchronized with changing data."
            )
        
        # Framework/Architecture questions
        elif any(phrase in q_lower for phrase in ["framework", "architecture", "design", "langchain", "langgraph", "system"]):
            return (
                f"I architect GenAI systems using LangChain and LangGraph for complex workflow orchestration. "
                f"At Mastercard, I designed event-driven agent architectures that process 50K+ daily transactions "
                f"with intelligent routing and decision-making capabilities. "
                f"\\n\\nMy architecture patterns include: modular agent design with specialized roles, "
                f"message-passing protocols for inter-agent communication, persistent state management for "
                f"long-running workflows, and fault-tolerant execution with automatic retry mechanisms. "
                f"\\n\\nI implemented MCP (Model Context Protocol) integration enabling seamless connections "
                f"between AI models, developer tools, and enterprise systems. This reduced development time "
                f"by 50% and improved system reliability. I also built custom tools extending LLM capabilities "
                f"across IDEs, databases, and internal knowledge bases, creating a unified AI development platform."
            )
        
        # Deployment/Production questions  
        elif any(phrase in q_lower for phrase in ["deploy", "production", "scale", "mlops", "cloud", "kubernetes"]):
            return (
                f"I manage end-to-end MLOps/LLMOps workflows for GenAI systems deployed on AWS SageMaker, "
                f"Azure OpenAI, and GCP Vertex AI. My production pipelines handle model training, evaluation, "
                f"deployment, and monitoring with automated CI/CD using Docker and Kubernetes. "
                f"\\n\\nAt Mastercard, I scaled systems to handle 10x traffic increases while maintaining "
                f"<100ms P95 latency. I implemented blue-green deployments for zero-downtime releases, "
                f"canary rollouts for risk mitigation, and comprehensive monitoring using Prometheus and Grafana. "
                f"\\n\\nKey production practices include: GPU resource optimization for cost efficiency, "
                f"model quantization and optimization for inference speed, drift detection with automatic "
                f"retraining triggers, and compliance frameworks ensuring responsible AI deployment. "
                f"I also maintain 99.9% uptime through redundant deployments and automated failover mechanisms."
            )
        
        # Technical challenge questions
        elif any(phrase in q_lower for phrase in ["challenge", "problem", "difficult", "issue", "troubleshoot"]):
            return (
                f"A significant challenge I faced was optimizing a multi-agent RAG system experiencing latency "
                f"spikes above 2 seconds during peak loads. The system served financial risk assessments where "
                f"sub-100ms response time was critical for user experience. "
                f"\\n\\nI diagnosed the issue through comprehensive profiling and found three bottlenecks: "
                f"inefficient vector similarity searches, redundant LLM calls across agents, and memory leaks "
                f"in the orchestration layer. My solution involved implementing semantic caching with Redis, "
                f"optimizing agent communication patterns, and introducing connection pooling. "
                f"\\n\\nThe results were dramatic: average response time dropped to 45ms, system throughput "
                f"increased by 300%, and memory usage stabilized. I also implemented predictive scaling "
                f"based on traffic patterns, preventing future performance degradation. This solution became "
                f"a template for other high-performance GenAI deployments across the organization."
            )
        
        # Project walkthrough questions
        elif any(phrase in q_lower for phrase in ["project", "walk through", "describe", "built", "developed"]):
            return (
                f"Let me describe a comprehensive agentic AI project I led at Mastercard for automated "
                f"financial document processing and compliance checking. "
                f"\\n\\n**Situation**: Manual document review was taking 2-3 days per case with 15% error rates. "
                f"We needed an automated system processing 1000+ documents daily while maintaining regulatory compliance. "
                f"\\n\\n**Task**: Design a multi-agent system integrating document parsing, risk assessment, "
                f"compliance verification, and exception handling with human-in-the-loop capabilities. "
                f"\\n\\n**Action**: I architected a LangGraph-based system with specialized agents: DocumentParser "
                f"using OCR and NLP, RiskAnalyzer with fine-tuned models, ComplianceChecker with regulatory rules, "
                f"and OrchestratorAgent managing the workflow. I integrated RAGAS evaluation ensuring 95% accuracy. "
                f"\\n\\n**Result**: Reduced processing time from 2 days to 15 minutes, achieved 97% accuracy, "
                f"cut operational costs by 60%, and maintained full audit trails for regulatory compliance. "
                f"The system now processes 5000+ documents monthly with minimal human intervention."
            )
        
        # Fine-tuning questions
        elif any(phrase in q_lower for phrase in ["fine-tune", "training", "model", "llm", "prompt"]):
            return (
                f"I have extensive experience fine-tuning LLMs for domain-specific applications using PyTorch "
                f"and Hugging Face Transformers. At T-Mobile, I fine-tuned GPT and LLaMA models on telecom-specific "
                f"datasets achieving 25% improvement in task-specific performance over base models. "
                f"\\n\\nMy approach includes: dataset curation with quality filters, advanced prompt engineering "
                f"using few-shot, Chain-of-Thought, and ReAct patterns, parameter-efficient fine-tuning with "
                f"LoRA and QLoRA to reduce computational costs, and comprehensive evaluation using RAGAS metrics. "
                f"\\n\\nI implemented sophisticated prompt engineering strategies including self-reflection "
                f"prompts for improved reasoning, guardrails for safety and bias mitigation, and dynamic "
                f"context selection based on query analysis. These optimizations improved response quality "
                f"by 40% while reducing token usage and inference costs by 30%."
            )
        
        # General technical questions
        else:
            return (
                f"Based on my {self.experience_years} years in GenAI and Agentic AI systems, I approach "
                f"technical challenges systematically using proven methodologies and cutting-edge frameworks. "
                f"My expertise spans the entire GenAI lifecycle from research and development through "
                f"production deployment and monitoring. "
                f"\\n\\nI specialize in LangChain, LangGraph, and CrewAI for building autonomous agent systems, "
                f"RAGAS framework for comprehensive LLM evaluation, and production deployment on cloud platforms "
                f"with MLOps best practices. My solutions consistently deliver measurable business impact "
                f"while maintaining high reliability and regulatory compliance. "
                f"\\n\\nI can provide specific examples from my work at Mastercard, John Deere, T-Mobile, "
                f"and Cisco where I've solved complex problems involving multi-agent coordination, "
                f"LLM optimization, vector database scaling, and responsible AI implementation."
            )

    def get_profile_summary(self) -> Dict:
        """Get comprehensive summary of the interview profile"""
        return {
            "name": self.name,
            "role": self.role,
            "experience_years": self.experience_years,
            "model": self.model,
            "llm_working": self.llm.is_working(),
            "education": self.education,
            "agentic_ai_expertise": self.agentic_ai_expertise,
            "llm_expertise": self.llm_expertise,
            "genai_frameworks": self.genai_frameworks,
            "vector_databases": self.vector_databases,
            "cloud_platforms": self.cloud_platforms,
            "mlops_tools": self.mlops_tools,
            "key_achievements": self.achievements,
            "work_experience": [exp["company"] + " - " + exp["role"] for exp in self.work_experience]
        }

# Factory function for backward compatibility
def make_llm():
    """Create interview-ready LLM client for Agentic AI Engineer role"""
    return InterviewProfile()