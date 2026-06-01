from sqlalchemy.orm import Session
from app.models.job_model import Job

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(
        self,
        title: str,
        description: str,
        company_id: int,
        uploaded_by: int,
        source_type: str = "text",
        extracted_text: str | None = None,
    ) -> Job:
        """Create a new job"""
        job = Job(
            title=title,
            description=description,
            company_id=company_id,
            uploaded_by=uploaded_by,
            source_type=source_type,
            extracted_text=extracted_text,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job_by_id(self, job_id: int) -> Job:
        """Get job by ID"""
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_jobs_by_user(self, user_id: int):
        """Get all jobs uploaded by a user"""
        return self.db.query(Job).filter(Job.uploaded_by == user_id).all()

    def update_job_risk_level(self, job_id: int, risk_level: str) -> Job:
        """Update job risk level"""
        job = self.get_job_by_id(job_id)
        if job:
            job.risk_level = risk_level
            self.db.commit()
            self.db.refresh(job)
        return job
