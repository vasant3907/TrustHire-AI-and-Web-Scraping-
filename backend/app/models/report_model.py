from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.core.database import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    ai_summary = Column(Text, nullable=True)
    trust_score = Column(Float, default=0.0)
    scam_probability = Column(Float, default=0.0)
    risk_level = Column(String(50), default="unknown")  # low, medium, high, critical
    recommendation = Column(Text, nullable=True)
    suspicious_keywords = Column(Text, nullable=True)  # JSON stored as text
    company_intelligence = Column(Text, nullable=True)  # JSON stored as text
    review_summary = Column(Text, nullable=True)
    company_presence_score = Column(Float, default=0.0)
    salary_validity = Column(String(50), nullable=True)  # valid, suspicious, invalid
    email_validity = Column(String(50), nullable=True)  # valid, suspicious, invalid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
