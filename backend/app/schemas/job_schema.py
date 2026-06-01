from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    title: str
    description: str
    company_id: Optional[int] = None
    source_type: Optional[str] = "text"
    extracted_text: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    source_type: Optional[str] = "text"
    extracted_text: Optional[str] = None
    company_id: Optional[int]
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[int] = None
