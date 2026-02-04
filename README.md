# 🚀 AI Resume Analyzer & Job Matcher

A complete production-ready AI application that analyzes resumes against job descriptions using advanced NLP, RAG (Retrieval Augmented Generation), and LLM technology.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Functionality
- **Resume Upload**: PDF resume parsing and text extraction
- **Job Description Analysis**: Intelligent requirement extraction
- **Match Score Calculation**: AI-powered compatibility percentage
- **Skills Extraction**: Automatic identification of technical and soft skills
- **Gap Analysis**: Identification of missing skills
- **Strength Assessment**: Highlights candidate's strong points
- **Personalized Suggestions**: Actionable improvement recommendations
- **AI Summary**: Concise executive summary of the analysis

### Technical Features
- **RAG Architecture**: Vector-based retrieval for context-aware analysis
- **FAISS Vector Database**: Efficient similarity search
- **OpenAI GPT Integration**: Advanced natural language understanding
- **Sentence Transformers**: State-of-the-art embeddings
- **REST API**: Clean, documented FastAPI backend
- **Modern UI**: Beautiful Gradio interface with custom styling

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework
- **LangChain**: LLM orchestration and chaining
- **FAISS**: Vector similarity search
- **OpenAI API**: GPT-3.5/4 for analysis
- **SentenceTransformers**: Text embeddings
- **PyPDF2**: PDF text extraction
- **Pydantic**: Data validation

### Frontend
- **Gradio**: Interactive web interface
- **Custom CSS**: Professional styling
- **Requests**: API communication

### AI/ML
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: GPT-3.5-turbo (configurable to GPT-4)
- **Vector DB**: FAISS with L2 distance

## 🏗️ Architecture

```
┌─────────────────┐
│   Gradio UI  │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │
│   (Backend)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────┐
    ▼         ▼          ▼        ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ PyPDF2 │ │ RAG  │ │ LLM  │ │Embed │
│Parser  │ │+FAISS│ │OpenAI│ │Model │
└────────┘ └──────┘ └──────┘ └──────┘
```

### Data Flow
1. User uploads PDF resume + pastes job description
2. FastAPI extracts text from PDF
3. Text is cleaned and chunked
4. Embeddings generated using SentenceTransformers
5. Chunks stored in FAISS vector database
6. Relevant chunks retrieved based on JD similarity
7. LLM analyzes resume vs JD using retrieved context
8. Results returned as structured JSON
9. Gradio displays formatted results

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- OpenAI API key (get from https://platform.openai.com/api-keys)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd resume_matcher
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Models
The first run will automatically download the embedding model (~80MB). This happens once.

## ⚙️ Configuration

### Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```bash
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional (defaults shown)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.3
MAX_TOKENS=2000
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=8501
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | - |
| `EMBEDDING_MODEL` | HuggingFace model for embeddings | all-MiniLM-L6-v2 |
| `LLM_MODEL` | OpenAI model (gpt-3.5-turbo or gpt-4) | gpt-3.5-turbo |
| `LLM_TEMPERATURE` | Creativity (0-1, lower = more focused) | 0.3 |
| `MAX_TOKENS` | Max response length | 2000 |
| `BACKEND_PORT` | FastAPI server port | 8000 |
| `FRONTEND_PORT` | Streamlit app port | 8501 |

## 🚀 Running the Application

### Method 1: Two Terminal Windows (Recommended for Development)

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run FastAPI backend
python -m backend.main
```

Expected output:
```
Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
Model loaded. Embedding dimension: 384
✓ Embedding service ready
✓ RAG service ready
✓ LLM service ready
All services initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Gradio frontend
python frontend/ui.py
```

Expected output:
```
You can now view your Gradio app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

### Method 2: Using Screen/Tmux (Production)
```bash
# Terminal 1
screen -S backend
python -m backend.main

# Detach with Ctrl+A, D

# Terminal 2
screen -S frontend
Python frontend/ui.py

# Detach with Ctrl+A, D
```

### Method 3: Docker (Optional)
```bash
# Coming soon - Docker compose setup
docker-compose up
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Resume Analyzer API is running",
  "version": "1.0.0"
}
```

#### 2. Analyze Resume
```http
POST /analyze
```

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `resume`: PDF file (required)
  - `job_description`: Text (required, min 10 chars)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=We are looking for a Python developer with experience in FastAPI..."
```

**Response (200 OK):**
```json
{
  "match_score": 75.5,
  "resume_skills": [
    "Python",
    "FastAPI",
    "Machine Learning",
    "SQL",
    "Docker"
  ],
  "jd_skills": [
    "Python",
    "FastAPI",
    "AWS",
    "Kubernetes",
    "CI/CD"
  ],
  "missing_skills": [
    "AWS",
    "Kubernetes",
    "CI/CD"
  ],
  "matched_skills": [
    "Python",
    "FastAPI"
  ],
  "strengths": [
    "Strong Python programming background",
    "Experience with FastAPI framework",
    "Good understanding of ML algorithms"
  ],
  "suggestions": [
    "Gain hands-on experience with AWS services",
    "Learn Kubernetes container orchestration",
    "Set up CI/CD pipelines using GitHub Actions"
  ],
  "summary": "Candidate shows strong foundation in Python and FastAPI with good potential. Recommended to focus on cloud technologies and DevOps practices to become a perfect match."
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "Only PDF files are supported"
}
```

500 Internal Server Error:
```json
{
  "error": "Internal server error",
  "detail": "Analysis failed: [error details]",
  "status_code": 500
}
```

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
resume_matcher/
│
├── backend/                    # Backend FastAPI application
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastAPI app and routes
│   ├── schemas.py             # Pydantic models
│   ├── embeddings.py          # Embedding generation service
│   ├── rag.py                 # RAG and vector store
│   └── llm.py                 # OpenAI LLM service
│
├── frontend/                   # Frontend Gradio application
│   └── ui.py                 # Gradio UI
│
├── data/                       # Data directory (auto-generated)
│   └── uploaded_resumes/      # Temporary PDF storage
│
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your environment variables (git-ignored)
└── README.md                 # This file
```

### File Descriptions

#### Backend Files

**`backend/main.py`** (FastAPI Application)
- Initializes FastAPI app with CORS
- Defines `/analyze` endpoint
- Handles PDF upload and text extraction
- Orchestrates RAG and LLM services
- Error handling and logging

**`backend/schemas.py`** (Data Models)
- `AnalysisRequest`: Request validation
- `AnalysisResponse`: Response structure
- `ErrorResponse`: Error formatting
- Uses Pydantic for validation

**`backend/embeddings.py`** (Embedding Service)
- Loads SentenceTransformer model
- Generates text embeddings
- Computes cosine similarity
- Singleton pattern for efficiency

**`backend/rag.py`** (RAG Implementation)
- `DocumentChunker`: Text cleaning and chunking
- `VectorStore`: FAISS index management
- `RAGService`: Main RAG orchestration
- Retrieves relevant context for LLM

**`backend/llm.py`** (LLM Service)
- OpenAI API integration
- Structured prompt engineering
- JSON response parsing
- Match score calculation

#### Frontend Files

**`frontend/ui.py`** (Gradio UI)
- Beautiful custom CSS styling
- File upload interface
- API communication
- Results visualization
- Progress indicators

## 🔬 How It Works

### Detailed Workflow

1. **PDF Processing**
   - User uploads resume PDF
   - PyPDF2 extracts text from all pages
   - Text validation ensures quality

2. **Text Preprocessing**
   - Remove extra whitespace and special characters
   - Normalize text format
   - Split into overlapping chunks (300 chars, 50 overlap)

3. **Embedding Generation**
   - Each chunk converted to 384-dim vector
   - Uses `all-MiniLM-L6-v2` model
   - Vectors stored in FAISS index

4. **Similarity Search**
   - Job description embedded
   - Top-K most similar resume chunks retrieved
   - Provides relevant context to LLM

5. **LLM Analysis**
   - GPT receives: retrieved chunks + full JD
   - Extracts skills from both documents
   - Compares and identifies gaps
   - Generates suggestions
   - Returns structured JSON

6. **Score Calculation**
   ```python
   match_score = (matched_skills / total_jd_skills) * 100
   ```

7. **Results Display**
   - Gradio renders beautiful UI
   - Color-coded skill badges
   - Progress bars for scores
   - Downloadable JSON report

### Match Score Logic

```python
# Example calculation
jd_skills = ["Python", "AWS", "Docker", "React"]  # 4 skills
matched_skills = ["Python", "Docker"]  # 2 matched

match_score = (2 / 4) * 100 = 50%
```

### Prompt Engineering

The system uses carefully crafted prompts:

```python
system_prompt = """You are an expert HR analyst and ATS specialist.
Extract skills, compare documents, identify gaps, and provide suggestions.
Return ONLY valid JSON with specific structure."""

user_prompt = f"""
RESUME: {resume_text}
JOB DESCRIPTION: {job_description}
Provide comprehensive analysis in JSON format.
"""
```

## 📸 Screenshots

### 1. Home Page
```
┌─────────────────────────────────────────┐
│  📄 AI Resume Analyzer & Job Matcher   │
│  Upload resume and paste job description│
├─────────────────────────────────────────┤
│  [Upload Resume PDF]                    │
│  [Paste Job Description]                │
│  [🚀 Analyze Resume]                    │
└─────────────────────────────────────────┘
```

### 2. Analysis Results
```
┌─────────────────────────────────────────┐
│  Match Score: 75%                       │
│  ████████████████░░░░░░                │
│  Good Match 👍                          │
├─────────────────────────────────────────┤
│  ✅ Matched Skills                      │
│  [Python] [FastAPI] [SQL]              │
│                                         │
│  ❌ Missing Skills                      │
│  [AWS] [Kubernetes] [Docker]           │
│                                         │
│  💪 Strengths                           │
│  • Strong Python background            │
│  • Good API design skills              │
│                                         │
│  💡 Suggestions                         │
│  • Learn AWS fundamentals              │
│  • Practice with Docker containers     │
└─────────────────────────────────────────┘
```

## 🚢 Deployment

### Local Deployment (Already Covered Above)
See "Running the Application" section.

### Production Deployment

#### Option 1: Traditional Server

1. **Set up server** (Ubuntu 20.04+ recommended)
```bash
sudo apt update
sudo apt install python3.9 python3-pip nginx
```

2. **Clone and setup**
```bash
git clone <repo-url>
cd resume_matcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure systemd services**

Create `/etc/systemd/system/resume-backend.service`:
```ini
[Unit]
Description=Resume Analyzer Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/resume_matcher
Environment="PATH=/path/to/resume_matcher/venv/bin"
ExecStart=/path/to/resume_matcher/venv/bin/python -m backend.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/resume-frontend.service`:
```ini
[Unit]
Description=Resume Analyzer Frontend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/resume_matcher
Environment="PATH=/path/to/resume_matcher/venv/bin"
ExecStart=/path/to/resume_matcher/venv/bin/streamlit run frontend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start services**
```bash
sudo systemctl daemon-reload
sudo systemctl enable resume-backend resume-frontend
sudo systemctl start resume-backend resume-frontend
```

5. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8000/;
    }

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### Option 2: Docker Deployment
```bash
# Coming soon
docker build -t resume-analyzer .
docker run -p 8000:8000 -p 8501:8501 resume-analyzer
```

#### Option 3: Cloud Platforms

**AWS EC2:**
1. Launch t2.medium instance (2GB RAM minimum)
2. Follow "Traditional Server" steps
3. Configure security groups (ports 8000, 8501)

**Google Cloud Run:**
- Containerize application
- Deploy as Cloud Run service
- Set environment variables

**Heroku:**
- Add Procfile
- Deploy via git push
- Configure buildpacks

## 🐛 Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"
**Solution:** 
```bash
# Make sure .env file exists and contains:
OPENAI_API_KEY=sk-your-key-here

# Reload environment:
source .env
```

#### 2. "Module not found" errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment is activated
which python  # Should point to venv
```

#### 3. "API Unavailable" in Streamlit
**Solution:**
```bash
# Check if backend is running:
curl http://localhost:8000/health

# If not, start backend:
python -m backend.main
```

#### 4. "Failed to extract text from PDF"
**Cause:** Scanned PDF or protected PDF
**Solution:**
- Use text-based PDFs (not scanned images)
- Remove password protection
- Try re-saving PDF from another program

#### 5. Slow first run
**Cause:** Downloading embedding model (~80MB)
**Solution:** Wait for initial download (one-time only)

#### 6. Out of memory errors
**Solution:**
```bash
# Reduce chunk size in rag.py:
chunk_text(text, chunk_size=200, overlap=30)

# Use smaller embedding model in .env:
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L3-v2
```

#### 7. OpenAI rate limits
**Solution:**
- Upgrade OpenAI plan
- Add retry logic
- Use GPT-3.5 instead of GPT-4

### Debug Mode

Enable verbose logging:
```python
# In backend/main.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips

1. **Use GPU for embeddings** (if available):
```python
# In embeddings.py:
model = SentenceTransformer(model_name, device='cuda')
```

2. **Cache API responses**:
```python
# Add caching decorator
from functools import lru_cache
```

3. **Optimize chunk size**:
- Smaller chunks = faster but less context
- Larger chunks = slower but better context
- Sweet spot: 300-500 characters

## 📊 Performance Metrics

- **PDF Processing**: ~1-2 seconds
- **Embedding Generation**: ~0.5 seconds
- **Vector Search**: ~0.1 seconds
- **LLM Analysis**: ~5-10 seconds
- **Total Time**: ~7-15 seconds per analysis

## 🔐 Security Considerations

1. **API Key Protection**
   - Never commit `.env` to git
   - Use environment variables
   - Rotate keys regularly

2. **File Upload Validation**
   - Only accept PDF files
   - Limit file size (10MB max recommended)
   - Scan for malware in production

3. **Rate Limiting**
   - Implement request throttling
   - Use API key quotas
   - Monitor usage patterns

4. **Data Privacy**
   - Don't store uploaded resumes long-term
   - Clear temporary files
   - Comply with GDPR/privacy laws

## 📝 Resume Best Practices

To get the best analysis results, resumes should:

1. **Use standard formatting**
   - Clear section headers
   - Bullet points for responsibilities
   - Consistent font and spacing

2. **Include keywords**
   - Technical skills section
   - Tools and technologies
   - Certifications and courses

3. **Be text-based**
   - Not scanned images
   - Searchable text
   - No password protection

4. **Quantify achievements**
   - Numbers and metrics
   - Impact statements
   - Concrete examples

Example good resume format:
```
John Doe
Software Engineer

SKILLS
- Programming: Python, JavaScript, SQL
- Frameworks: FastAPI, React, Django
- Tools: Docker, Git, AWS

EXPERIENCE
Senior Developer | Tech Corp | 2020-Present
• Built REST APIs using FastAPI serving 10K requests/day
• Reduced deployment time by 60% using Docker
• Led team of 5 developers on ML project
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Senior AI Engineer Team
- Full Stack Architecture Team

## 🙏 Acknowledgments

- OpenAI for GPT API
- HuggingFace for Sentence Transformers
- FastAPI and Streamlit communities
- FAISS team at Facebook Research

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check troubleshooting section
- Review API documentation

## 🗺️ Roadmap

- [ ] Docker containerization
- [ ] Multi-language support
- [ ] Batch processing
- [ ] Resume builder integration
- [ ] Interview question generator
- [ ] Salary estimation
- [ ] Company fit analysis
- [ ] Chrome extension

---

**Built with ❤️ using FastAPI, Streamlit, and AI**
