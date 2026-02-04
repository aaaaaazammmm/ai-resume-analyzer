"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    job_description: str = Field(..., min_length=10, description="Job description text")
    

class SkillItem(BaseModel):
    """Individual skill with confidence score"""
    name: str
    category: Optional[str] = None
    confidence: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    match_score: float = Field(..., ge=0, le=100, description="Match percentage")
    resume_skills: List[str] = Field(default_factory=list)
    jd_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    summary: str = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 75.5,
                "resume_skills": ["Python", "Machine Learning", "SQL"],
                "jd_skills": ["Python", "Java", "AWS", "Docker"],
                "missing_skills": ["Java", "AWS", "Docker"],
                "matched_skills": ["Python"],
                "strengths": ["Strong Python background", "ML expertise"],
                "suggestions": ["Learn Java basics", "Get AWS certification"],
                "summary": "Good match with room for improvement in cloud technologies"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int = 400
