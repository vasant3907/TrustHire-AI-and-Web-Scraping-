import json
import re
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job_model import Job
from app.models.report_model import AnalysisReport
from app.models.uploaded_file_model import UploadedFile as UploadedFileModel
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_user
from app.schemas.report_schema import ReportResponse
from app.services.ai_service import AIService
from app.services.pdf_service import build_report_pdf
from app.services.scraping_service import ScrapingService
from app.models.feature_model import AlertLog, UserReportNote

router = APIRouter(prefix="/api/reports", tags=["reports"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


def _build_and_save_report(job: Job, db: Session) -> AnalysisReport:
    scraper = ScrapingService()
    company_context = scraper.scrape_company_info(job.title)

    ai_service = AIService()
    review_summary = ai_service.summarize_reviews(job.title, company_context.get("reviews", []))
    company_context["review_summary"] = review_summary

    analysis = ai_service.analyze_job_description(
        f"Job title/company: {job.title}\n\nJob description:\n{job.description}",
        company_context=company_context,
    )

    report_data = {
        "trust_score": analysis["trust_score"],
        "scam_probability": analysis.get("scam_probability", max(0.0, 100.0 - analysis["trust_score"])),
        "risk_level": analysis["risk_level"],
        "ai_summary": f"{analysis['ai_summary']} Source: {analysis.get('analysis_source', 'ai')}.",
        "recommendation": analysis["recommendation"],
        "suspicious_keywords": json.dumps(analysis.get("suspicious_keywords", [])),
        "company_intelligence": json.dumps(company_context),
        "review_summary": review_summary,
        "company_presence_score": 85.0 if company_context.get("website") else 55.0 if company_context.get("search_results") else 35.0,
        "salary_validity": analysis.get("salary_validity", "valid"),
        "email_validity": analysis.get("email_validity", "valid"),
    }

    report = AnalysisReport(job_id=job.id, **report_data)
    job.risk_level = analysis["risk_level"]
    db.add(report)
    db.flush()
    if report.risk_level in {"high", "critical"}:
        db.add(
            AlertLog(
                report_id=report.id,
                user_id=job.uploaded_by,
                message=f"{report.risk_level.title()} risk job report created with {report.scam_probability:.0f}% scam probability.",
            )
        )
    db.commit()
    db.refresh(report)
    return report


@router.get("/my-reports", response_model=list[ReportResponse])
def get_my_reports(
    risk_level: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id)
    )
    if risk_level:
        query = query.filter(AnalysisReport.risk_level == risk_level)
    return query.order_by(AnalysisReport.created_at.desc()).all()


@router.get("/download/{report_id}")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id, AnalysisReport.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    payload = {
        "id": report.id,
        "job_id": report.job_id,
        "trust_score": report.trust_score,
        "scam_probability": report.scam_probability,
        "risk_level": report.risk_level,
        "ai_summary": report.ai_summary,
        "recommendation": report.recommendation,
        "suspicious_keywords": json.loads(report.suspicious_keywords or "[]"),
        "review_summary": report.review_summary,
        "company_intelligence": json.loads(report.company_intelligence or "{}"),
        "created_at": report.created_at.isoformat() if report.created_at else None,
    }
    content = json.dumps(payload, indent=2)
    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=trusthire-report-{report.id}.json"},
    )


@router.get("/pdf/{report_id}")
def download_report_pdf(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id, AnalysisReport.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return Response(
        content=build_report_pdf(report),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=trusthire-report-{report.id}.pdf"},
    )


@router.get("/{report_id}/timeline")
def report_timeline(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id, AnalysisReport.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    keywords = json.loads(report.suspicious_keywords or "[]")
    intelligence = json.loads(report.company_intelligence or "{}")
    return [
        {"step": "Input captured", "detail": "Job text and/or screenshot OCR text was stored."},
        {"step": "Public intelligence collected", "detail": f"{len(intelligence.get('reviews', []))} review links and {len(intelligence.get('public_mentions', []))} public mentions found."},
        {"step": "Fraud signals detected", "detail": ", ".join(keywords) if keywords else "No keyword-level scam signals found."},
        {"step": "AI risk reasoning", "detail": report.ai_summary},
        {"step": "Recommendation generated", "detail": report.recommendation},
    ]


@router.post("/{report_id}/notes")
def save_report_note(
    report_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id, AnalysisReport.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    note = (
        db.query(UserReportNote)
        .filter(UserReportNote.report_id == report_id, UserReportNote.user_id == current_user.id)
        .first()
    )
    if not note:
        note = UserReportNote(report_id=report_id, user_id=current_user.id)
        db.add(note)
    note.note = payload.get("note", "")
    note.bookmarked = bool(payload.get("bookmarked", False))
    db.commit()
    return {"message": "saved", "note": note.note, "bookmarked": note.bookmarked}


@router.get("/{report_id}/notes")
def get_report_note(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id, AnalysisReport.id == report_id)
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    note = (
        db.query(UserReportNote)
        .filter(UserReportNote.report_id == report_id, UserReportNote.user_id == current_user.id)
        .first()
    )
    return {
        "note": note.note if note else "",
        "bookmarked": bool(note.bookmarked) if note else False,
    }


@router.post("/analyze-upload", response_model=ReportResponse)
async def analyze_uploaded_job(
    company_name: str = Form("Unknown Company"),
    job_description: str = Form(""),
    screenshot: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_service = AIService()
    extracted_text = ""
    upload_record = None

    if screenshot:
        if not screenshot.content_type or not screenshot.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image screenshots are supported")

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        raw = await screenshot.read()
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", screenshot.filename or "screenshot.png").strip(".-")
        stored_filename = f"{uuid.uuid4().hex}-{safe_name or 'screenshot.png'}"
        file_path = UPLOAD_DIR / stored_filename
        try:
            file_path.write_bytes(raw)
        except OSError:
            # OCR can still run from memory; do not fail the whole analysis if local file persistence is blocked.
            file_path = UPLOAD_DIR / f"not-saved-{stored_filename}"

        ocr = ai_service.extract_text_from_image(raw, screenshot.content_type)
        extracted_text = ocr.get("text", "")
        upload_record = UploadedFileModel(
            original_filename=screenshot.filename or "screenshot",
            stored_filename=stored_filename,
            content_type=screenshot.content_type,
            file_path=str(file_path),
            extracted_text=extracted_text,
            uploaded_by=current_user.id,
        )
        db.add(upload_record)
        db.flush()

    combined_description = "\n\n".join(part for part in [job_description.strip(), extracted_text.strip()] if part)
    if screenshot and not combined_description:
        combined_description = (
            "A screenshot was uploaded, but OCR could not extract readable job text from it. "
            "The image may be blurry, low contrast, cropped, handwritten, or the AI OCR provider may be unavailable. "
            "Ask the user to verify the company/recruiter manually and paste the job text for higher-confidence analysis."
        )
    if not combined_description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Add a job description or upload a readable screenshot")

    job = Job(
        title=company_name.strip() or "Unknown Company",
        description=combined_description,
        source_type="mixed" if job_description and extracted_text else "screenshot" if extracted_text else "text",
        extracted_text=extracted_text or None,
        uploaded_by=current_user.id,
    )
    db.add(job)
    db.flush()
    if upload_record:
        upload_record.job_id = job.id

    return _build_and_save_report(job, db)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analysis report"""
    report = (
        db.query(AnalysisReport)
        .join(Job, AnalysisReport.job_id == Job.id)
        .filter(Job.uploaded_by == current_user.id)
        .filter((AnalysisReport.id == report_id) | (AnalysisReport.job_id == report_id))
        .order_by(AnalysisReport.created_at.desc())
        .first()
    )
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report

@router.post("/analyze/{job_id}", response_model=ReportResponse)
def analyze_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger job analysis"""
    job = db.query(Job).filter(Job.id == job_id, Job.uploaded_by == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return _build_and_save_report(job, db)
