from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    source_type = Column(String(50), default="text")  # text, screenshot, mixed
    extracted_text = Column(Text, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    risk_level = Column(String(50), default="unknown")  # low, medium, high, critical
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
