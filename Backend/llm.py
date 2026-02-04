"""
LLM module for interacting with OpenAI API
"""
import os
import json
from typing import Dict, Any
from openai import OpenAI


class LLMService:
    """Service for LLM-based analysis"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
    
    def analyze_resume_vs_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description using LLM
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description text
            
        Returns:
            Dictionary with analysis results
        """
        system_prompt = """You are an expert HR analyst and ATS (Applicant Tracking System) specialist.
Your job is to analyze resumes against job descriptions and provide detailed, actionable feedback.

You MUST return your response as a valid JSON object with the following structure:
{
    "resume_skills": ["skill1", "skill2", ...],
    "jd_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "matched_skills": ["skill1", "skill2", ...],
    "strengths": ["strength1", "strength2", ...],
    "suggestions": ["suggestion1", "suggestion2", ...],
    "summary": "Brief 2-3 sentence summary of the analysis"
}

Guidelines:
- Extract ALL technical and soft skills from both documents
- Be specific and granular (e.g., "Python 3.x" not just "Python")
- Identify missing skills critical for the role
- Highlight 3-5 key strengths from the resume
- Provide 3-5 actionable improvement suggestions
- Keep summary concise and professional
- Return ONLY valid JSON, no markdown or extra text
"""
        
        user_prompt = f"""Analyze the following resume against the job description:

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}

Provide a comprehensive analysis in JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Validate and normalize response
            return self._normalize_response(result)
            
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            raise
    
    def _normalize_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate LLM response"""
        normalized = {
            "resume_skills": result.get("resume_skills", []),
            "jd_skills": result.get("jd_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "matched_skills": result.get("matched_skills", []),
            "strengths": result.get("strengths", []),
            "suggestions": result.get("suggestions", []),
            "summary": result.get("summary", "Analysis completed successfully")
        }
        
        # Ensure all lists are actually lists
        for key in ["resume_skills", "jd_skills", "missing_skills", "matched_skills", "strengths", "suggestions"]:
            if not isinstance(normalized[key], list):
                normalized[key] = []
        
        return normalized
    
    def calculate_match_score(self, matched_skills: list, jd_skills: list) -> float:
        """
        Calculate match percentage
        
        Args:
            matched_skills: List of matched skills
            jd_skills: List of all JD skills
            
        Returns:
            Match score as percentage (0-100)
        """
        if not jd_skills:
            return 0.0
        
        matched_count = len(matched_skills)
        total_count = len(jd_skills)
        
        score = (matched_count / total_count) * 100
        return round(score, 2)


# Global instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
