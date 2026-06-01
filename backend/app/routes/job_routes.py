from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_user
from app.repositories.job_repository import JobRepository
from app.schemas.job_schema import JobCreate, JobResponse

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job"""
    job_repo = JobRepository(db)
    job = job_repo.create_job(
        title=job_data.title,
        description=job_data.description,
        company_id=job_data.company_id,
        uploaded_by=current_user.id,
        source_type=job_data.source_type or "text",
        extracted_text=job_data.extracted_text
    )
    return job

@router.get("/my-jobs", response_model=list[JobResponse])
def get_my_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all jobs uploaded by current user"""
    job_repo = JobRepository(db)
    jobs = job_repo.get_jobs_by_user(current_user.id)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get job by ID"""
    job_repo = JobRepository(db)
    job = job_repo.get_job_by_id(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job
