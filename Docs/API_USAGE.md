# 📡 API Usage Guide

Complete guide for interacting with the Resume Analyzer API programmatically.

## Table of Contents
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
- [Request Examples](#request-examples)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Code Examples](#code-examples)
- [Rate Limiting](#rate-limiting)

## Authentication

Currently, the API is open (no authentication required for local deployment).

For production, you should add API key authentication:
```python
# Example: Add to headers
headers = {"X-API-Key": "your-secret-key"}
```

## Base URL

**Local Development:**
```
http://localhost:8000
```

**Production:**
```
https://your-domain.com/api
```

## Endpoints

### 1. Health Check

**GET** `/`
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Resume Analyzer API is running",
  "version": "1.0.0"
}
```

---

### 2. Detailed Health Check

**GET** `/health`
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "embedding": "ready",
    "rag": "ready",
    "llm": "ready"
  }
}
```

---

### 3. Analyze Resume

**POST** `/analyze`

**Headers:**
- Content-Type: `multipart/form-data`

**Form Data:**
- `resume`: PDF file (required)
- `job_description`: Text (required, min 10 characters)

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=We are looking for a Python developer with 5+ years experience..."
```

**Success Response (200 OK):**
```json
{
  "match_score": 75.5,
  "resume_skills": [
    "Python",
    "FastAPI",
    "Machine Learning",
    "SQL",
    "Docker",
    "AWS",
    "Git",
    "REST APIs",
    "TensorFlow",
    "Pandas"
  ],
  "jd_skills": [
    "Python",
    "FastAPI",
    "AWS",
    "Kubernetes",
    "CI/CD",
    "Docker",
    "PostgreSQL",
    "Redis"
  ],
  "missing_skills": [
    "Kubernetes",
    "CI/CD",
    "Redis"
  ],
  "matched_skills": [
    "Python",
    "FastAPI",
    "AWS",
    "Docker"
  ],
  "strengths": [
    "Strong Python programming background with 5+ years experience",
    "Extensive experience with FastAPI framework",
    "Good understanding of cloud platforms, particularly AWS"
  ],
  "suggestions": [
    "Gain hands-on experience with Kubernetes container orchestration",
    "Learn to set up CI/CD pipelines using Jenkins or GitHub Actions",
    "Familiarize yourself with Redis caching patterns"
  ],
  "summary": "Strong candidate with solid Python and API development skills. Matches 50% of required skills. Recommended to focus on container orchestration and DevOps practices to become an ideal fit."
}
```

**Error Responses:**

*400 Bad Request - Invalid file type:*
```json
{
  "detail": "Only PDF files are supported"
}
```

*400 Bad Request - Missing job description:*
```json
{
  "detail": "Job description must be at least 10 characters"
}
```

*400 Bad Request - Empty or corrupted PDF:*
```json
{
  "detail": "Failed to extract text from PDF: No text could be extracted"
}
```

*500 Internal Server Error:*
```json
{
  "error": "Internal server error",
  "detail": "Analysis failed: [detailed error message]",
  "status_code": 500
}
```

## Request Examples

### Python with requests

```python
import requests

def analyze_resume(resume_path, job_description):
    """Analyze resume against job description"""
    
    url = "http://localhost:8000/analyze"
    
    # Prepare files and data
    files = {
        'resume': ('resume.pdf', open(resume_path, 'rb'), 'application/pdf')
    }
    data = {
        'job_description': job_description
    }
    
    # Make request
    response = requests.post(url, files=files, data=data)
    
    # Check response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.json()}")

# Usage
job_desc = """
We are seeking a Senior Python Developer with expertise in:
- Python, FastAPI, Django
- AWS, Docker, Kubernetes
- PostgreSQL, Redis
- CI/CD pipelines
"""

result = analyze_resume('my_resume.pdf', job_desc)
print(f"Match Score: {result['match_score']}%")
print(f"Missing Skills: {', '.join(result['missing_skills'])}")
```

### Python with httpx (async)

```python
import httpx
import asyncio

async def analyze_resume_async(resume_path, job_description):
    """Async resume analysis"""
    
    url = "http://localhost:8000/analyze"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        files = {
            'resume': ('resume.pdf', open(resume_path, 'rb'), 'application/pdf')
        }
        data = {
            'job_description': job_description
        }
        
        response = await client.post(url, files=files, data=data)
        return response.json()

# Usage
result = asyncio.run(analyze_resume_async('resume.pdf', job_desc))
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function analyzeResume(resumePath, jobDescription) {
    const form = new FormData();
    form.append('resume', fs.createReadStream(resumePath));
    form.append('job_description', jobDescription);
    
    try {
        const response = await axios.post(
            'http://localhost:8000/analyze',
            form,
            {
                headers: form.getHeaders(),
                timeout: 60000
            }
        );
        
        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        throw error;
    }
}

// Usage
const jobDesc = `
We need a Python developer with FastAPI experience...
`;

analyzeResume('./resume.pdf', jobDesc)
    .then(result => {
        console.log('Match Score:', result.match_score);
        console.log('Missing Skills:', result.missing_skills);
    })
    .catch(err => console.error(err));
```

### cURL (Shell Script)

```bash
#!/bin/bash

RESUME_PATH="./my_resume.pdf"
API_URL="http://localhost:8000/analyze"

# Job description (multiline)
JOB_DESC="We are seeking a Senior Python Developer with:
- 5+ years Python experience
- FastAPI or Django
- AWS cloud experience
- Docker and Kubernetes
- PostgreSQL database
"

# Make request
response=$(curl -s -X POST "$API_URL" \
  -F "resume=@$RESUME_PATH" \
  -F "job_description=$JOB_DESC")

# Parse response
echo "$response" | jq '.'

# Extract match score
match_score=$(echo "$response" | jq -r '.match_score')
echo "Match Score: $match_score%"
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "mime/multipart"
    "net/http"
    "os"
)

type AnalysisResponse struct {
    MatchScore     float64  `json:"match_score"`
    ResumeSkills   []string `json:"resume_skills"`
    JDSkills       []string `json:"jd_skills"`
    MissingSkills  []string `json:"missing_skills"`
    MatchedSkills  []string `json:"matched_skills"`
    Strengths      []string `json:"strengths"`
    Suggestions    []string `json:"suggestions"`
    Summary        string   `json:"summary"`
}

func analyzeResume(resumePath, jobDescription string) (*AnalysisResponse, error) {
    // Create multipart form
    body := &bytes.Buffer{}
    writer := multipart.NewWriter(body)
    
    // Add resume file
    file, err := os.Open(resumePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()
    
    part, err := writer.CreateFormFile("resume", "resume.pdf")
    if err != nil {
        return nil, err
    }
    io.Copy(part, file)
    
    // Add job description
    writer.WriteField("job_description", jobDescription)
    writer.Close()
    
    // Make request
    req, err := http.NewRequest("POST", "http://localhost:8000/analyze", body)
    if err != nil {
        return nil, err
    }
    req.Header.Set("Content-Type", writer.FormDataContentType())
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    // Parse response
    var result AnalysisResponse
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

func main() {
    jobDesc := `We need a Python developer with FastAPI experience...`
    
    result, err := analyzeResume("resume.pdf", jobDesc)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Match Score: %.2f%%\n", result.MatchScore)
    fmt.Printf("Missing Skills: %v\n", result.MissingSkills)
}
```

## Response Format

All successful responses return JSON with consistent structure:

```typescript
{
  match_score: number;        // 0-100
  resume_skills: string[];    // Skills found in resume
  jd_skills: string[];        // Skills required by job
  missing_skills: string[];   // Skills you need to learn
  matched_skills: string[];   // Skills you have that match
  strengths: string[];        // Your strong areas (3-5 items)
  suggestions: string[];      // Improvement tips (3-5 items)
  summary: string;            // Executive summary
}
```

## Error Handling

### Best Practices

```python
import requests

def safe_analyze(resume_path, job_description, max_retries=3):
    """Analyze with error handling and retries"""
    
    url = "http://localhost:8000/analyze"
    
    for attempt in range(max_retries):
        try:
            files = {
                'resume': ('resume.pdf', open(resume_path, 'rb'), 'application/pdf')
            }
            data = {'job_description': job_description}
            
            response = requests.post(
                url,
                files=files,
                data=data,
                timeout=60
            )
            
            # Check status code
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                # Bad request - don't retry
                error = response.json()
                raise ValueError(f"Invalid request: {error.get('detail')}")
            elif response.status_code == 500:
                # Server error - retry
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception("Server error after retries")
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                continue
            raise Exception("Request timeout")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to API server")
    
    raise Exception("Max retries exceeded")
```

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:

```python
# Example rate limit configuration
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze")
@limiter.limit("10/minute")  # 10 requests per minute
async def analyze_resume(...):
    ...
```

## Batch Processing

For analyzing multiple resumes:

```python
import concurrent.futures
from typing import List, Dict

def batch_analyze(resume_paths: List[str], job_description: str) -> List[Dict]:
    """Analyze multiple resumes concurrently"""
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(analyze_resume, path, job_description): path
            for path in resume_paths
        }
        
        for future in concurrent.futures.as_completed(futures):
            path = futures[future]
            try:
                result = future.result()
                results.append({
                    'path': path,
                    'analysis': result
                })
            except Exception as e:
                results.append({
                    'path': path,
                    'error': str(e)
                })
    
    return results

# Usage
resumes = ['resume1.pdf', 'resume2.pdf', 'resume3.pdf']
job_desc = "Python developer with FastAPI..."

results = batch_analyze(resumes, job_desc)

# Filter candidates by match score
good_matches = [
    r for r in results
    if 'analysis' in r and r['analysis']['match_score'] >= 70
]
```

## Webhooks (Future Feature)

For long-running analysis, webhooks could be implemented:

```python
# POST /analyze with callback
{
    "resume": file,
    "job_description": "...",
    "webhook_url": "https://your-app.com/webhook"
}

# Later, receive POST at webhook_url:
{
    "job_id": "uuid",
    "status": "completed",
    "result": { ... }
}
```

## Testing with Postman

1. **Create Collection:** "Resume Analyzer API"

2. **Add Health Check Request:**
   - Method: GET
   - URL: `http://localhost:8000/health`

3. **Add Analyze Request:**
   - Method: POST
   - URL: `http://localhost:8000/analyze`
   - Body: form-data
     - Key: `resume`, Type: File, Value: [select PDF]
     - Key: `job_description`, Type: Text, Value: [paste JD]

4. **Save and Run**

## Performance Tips

1. **Keep connections alive:**
   ```python
   session = requests.Session()
   session.post(url, ...)  # Reuse connection
   ```

2. **Use async for multiple requests:**
   ```python
   async with httpx.AsyncClient() as client:
       tasks = [client.post(...) for _ in range(10)]
       results = await asyncio.gather(*tasks)
   ```

3. **Stream large files:**
   ```python
   with open(large_file, 'rb') as f:
       files = {'resume': f}
       response = requests.post(url, files=files, stream=True)
   ```

## Cost Monitoring

Track API usage to monitor OpenAI costs:

```python
total_requests = 0
total_cost = 0.004  # per request average

def analyze_with_tracking(resume_path, job_description):
    global total_requests, total_cost
    
    result = analyze_resume(resume_path, job_description)
    
    total_requests += 1
    estimated_cost = total_requests * 0.004
    
    print(f"Total requests: {total_requests}")
    print(f"Estimated cost: ${estimated_cost:.2f}")
    
    return result
```

---

**For more examples and integration patterns, see the source code in `backend/main.py`**
