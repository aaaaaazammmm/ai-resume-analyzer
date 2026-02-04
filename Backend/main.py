"""
FastAPI Backend for AI Resume Analyzer
"""

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO

from schemas import AnalysisResponse, ErrorResponse
from rag import get_rag_service
from llm import get_llm_service
from embeddings import get_embedding_service

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Analyze resumes against job descriptions using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(pdf_file: bytes) -> str:
    """
    Extract text from PDF file
    
    Args:
        pdf_file: PDF file bytes
        
    Returns:
        Extracted text
    """
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise ValueError("No text could be extracted from PDF")
        
        return text
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("Initializing services...")
    try:
        # Initialize embedding service
        get_embedding_service()
        print("✓ Embedding service ready")
        
        # Initialize RAG service
        get_rag_service()
        print("✓ RAG service ready")
        
        # Initialize LLM service
        get_llm_service()
        print("✓ LLM service ready")
        
        print("All services initialized successfully!")
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Resume Analyzer API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "embedding": "ready",
            "rag": "ready",
            "llm": "ready"
        }
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze resume against job description
    
    Args:
        resume: Uploaded PDF file
        job_description: Job description text
        
    Returns:
        Analysis results with match score, skills, and suggestions
    """
    try:
        # Validate inputs
        if not resume.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        if not job_description or len(job_description.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 10 characters"
            )
        
        # Read PDF file
        pdf_content = await resume.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )
        
        # Extract text from PDF
        print("Extracting text from PDF...")
        resume_text = extract_text_from_pdf(pdf_content)
        
        if len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume text is too short or could not be extracted properly"
            )
        
        # Process resume with RAG
        print("Processing resume with RAG...")
        rag_service = get_rag_service()
        cleaned_resume = rag_service.process_resume(resume_text)
        
        # Retrieve relevant context
        print("Retrieving relevant context...")
        relevant_context = rag_service.retrieve_relevant_context(job_description, k=5)
        
        # Combine full resume with retrieved context for better analysis
        enhanced_resume = f"{relevant_context}\n\n{cleaned_resume[:3000]}"
        
        # Analyze with LLM
        print("Analyzing with LLM...")
        llm_service = get_llm_service()
        analysis_result = llm_service.analyze_resume_vs_job(enhanced_resume, job_description)
        
        # Calculate match score
        match_score = llm_service.calculate_match_score(
            analysis_result["matched_skills"],
            analysis_result["jd_skills"]
        )
        
        # Build response
        response = AnalysisResponse(
            match_score=match_score,
            resume_skills=analysis_result["resume_skills"],
            jd_skills=analysis_result["jd_skills"],
            missing_skills=analysis_result["missing_skills"],
            matched_skills=analysis_result["matched_skills"],
            strengths=analysis_result["strengths"],
            suggestions=analysis_result["suggestions"],
            summary=analysis_result["summary"]
        )
        
        print(f"Analysis complete. Match score: {match_score}%")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            status_code=500
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
