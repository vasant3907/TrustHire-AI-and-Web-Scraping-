from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportCreate(BaseModel):
    job_id: int

class ReportResponse(BaseModel):
    id: int
    job_id: int
    ai_summary: Optional[str]
    trust_score: float
    scam_probability: float = 0.0
    risk_level: str
    recommendation: Optional[str]
    suspicious_keywords: Optional[str]
    company_intelligence: Optional[str] = None
    review_summary: Optional[str] = None
    company_presence_score: float
    salary_validity: Optional[str]
    email_validity: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
