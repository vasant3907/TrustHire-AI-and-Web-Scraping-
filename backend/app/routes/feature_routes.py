from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.feature_model import AlertLog, CommunityScamReport, WatchlistEntry
from app.models.user_model import User
from app.services.verification_service import VerificationService

router = APIRouter(prefix="/api/features", tags=["features"])


@router.post("/community-reports")
def create_community_report(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    description = (payload.get("description") or "").strip()
    company_name = (payload.get("company_name") or "Unknown Company").strip()
    if not description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description is required")
    report = CommunityScamReport(
        company_name=company_name,
        recruiter_email=payload.get("recruiter_email"),
        platform=payload.get("platform"),
        description=description,
        evidence_url=payload.get("evidence_url"),
        reported_by=current_user.id,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"id": report.id, "message": "Community scam report submitted"}


@router.get("/community-reports")
def list_community_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reports = db.query(CommunityScamReport).order_by(CommunityScamReport.created_at.desc()).limit(100).all()
    return [
        {
            "id": report.id,
            "company_name": report.company_name,
            "recruiter_email": report.recruiter_email,
            "platform": report.platform,
            "status": report.status,
            "created_at": report.created_at,
        }
        for report in reports
    ]


@router.post("/verify-email")
def verify_email_domain(
    payload: dict,
    current_user: User = Depends(get_current_user),
):
    return VerificationService().verify_domain(payload.get("email", ""), payload.get("company_name", ""))


@router.post("/watchlist")
def add_watchlist_entry(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = WatchlistEntry(
        company_name=(payload.get("company_name") or "Unknown Company").strip(),
        recruiter_email=payload.get("recruiter_email"),
        reason=(payload.get("reason") or "User added watchlist entry").strip(),
        severity=payload.get("severity", "medium"),
        created_by=current_user.id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "message": "Watchlist entry added"}


@router.get("/watchlist")
def list_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = db.query(WatchlistEntry).order_by(WatchlistEntry.created_at.desc()).limit(100).all()
    return [
        {
            "id": entry.id,
            "company_name": entry.company_name,
            "recruiter_email": entry.recruiter_email,
            "reason": entry.reason,
            "severity": entry.severity,
            "created_at": entry.created_at,
        }
        for entry in entries
    ]


@router.get("/alerts")
def list_my_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alerts = (
        db.query(AlertLog)
        .filter(AlertLog.user_id == current_user.id)
        .order_by(AlertLog.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": alert.id,
            "report_id": alert.report_id,
            "message": alert.message,
            "admin_handled": bool(alert.sent),
            "created_at": alert.created_at,
        }
        for alert in alerts
    ]
