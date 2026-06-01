from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.feature_model import AlertLog, CommunityScamReport, WatchlistEntry
from app.models.job_model import Job
from app.models.report_model import AnalysisReport
from app.models.user_model import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    admin_emails = {email.strip().lower() for email in settings.ADMIN_EMAILS.split(",") if email.strip()}
    if current_user.id == 1 or current_user.email.lower() in admin_emails:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")


@router.get("/summary")
def admin_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    reports = db.query(AnalysisReport).all()
    users = db.query(User).count()
    jobs = db.query(Job).count()
    risk_counts = Counter(report.risk_level for report in reports)
    keyword_counts = Counter()
    for report in reports:
        try:
            import json
            keyword_counts.update(json.loads(report.suspicious_keywords or "[]"))
        except Exception:
            pass
    return {
        "users": users,
        "jobs": jobs,
        "reports": len(reports),
        "risk_counts": dict(risk_counts),
        "top_keywords": keyword_counts.most_common(8),
        "community_reports": db.query(CommunityScamReport).count(),
        "watchlist_entries": db.query(WatchlistEntry).count(),
        "alerts": db.query(AlertLog).count(),
    }


@router.get("/reports")
def admin_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    reports = db.query(AnalysisReport).order_by(AnalysisReport.created_at.desc()).limit(100).all()
    return [
        {
            "id": report.id,
            "job_id": report.job_id,
            "risk_level": report.risk_level,
            "trust_score": report.trust_score,
            "scam_probability": report.scam_probability,
            "created_at": report.created_at,
        }
        for report in reports
    ]


@router.get("/users")
def admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return [
        {"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at}
        for user in db.query(User).order_by(User.created_at.desc()).limit(100).all()
    ]


@router.get("/community-reports")
def admin_community_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    reports = db.query(CommunityScamReport).order_by(CommunityScamReport.created_at.desc()).limit(100).all()
    return [
        {
            "id": report.id,
            "company_name": report.company_name,
            "recruiter_email": report.recruiter_email,
            "platform": report.platform,
            "description": report.description,
            "evidence_url": report.evidence_url,
            "status": report.status,
            "reported_by": report.reported_by,
            "created_at": report.created_at,
        }
        for report in reports
    ]


@router.get("/watchlist")
def admin_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    entries = db.query(WatchlistEntry).order_by(WatchlistEntry.created_at.desc()).limit(100).all()
    return [
        {
            "id": entry.id,
            "company_name": entry.company_name,
            "recruiter_email": entry.recruiter_email,
            "reason": entry.reason,
            "severity": entry.severity,
            "created_by": entry.created_by,
            "created_at": entry.created_at,
        }
        for entry in entries
    ]


@router.get("/alerts")
def admin_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    alerts = db.query(AlertLog).order_by(AlertLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": alert.id,
            "report_id": alert.report_id,
            "user_id": alert.user_id,
            "channel": alert.channel,
            "message": alert.message,
            "sent": alert.sent,
            "created_at": alert.created_at,
        }
        for alert in alerts
    ]


@router.patch("/community-reports/{report_id}/status")
def update_community_report_status(
    report_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    allowed_statuses = {"submitted", "reviewing", "verified", "rejected"}
    next_status = (payload.get("status") or "").strip().lower()
    if next_status not in allowed_statuses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid report status")

    report = db.query(CommunityScamReport).filter(CommunityScamReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community report not found")

    report.status = next_status
    db.commit()
    db.refresh(report)
    return {"id": report.id, "status": report.status, "message": "Community report status updated"}


@router.patch("/alerts/{alert_id}/handled")
def mark_alert_handled(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    alert = db.query(AlertLog).filter(AlertLog.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    alert.sent = True
    db.commit()
    db.refresh(alert)
    return {"id": alert.id, "sent": alert.sent, "message": "Alert marked as handled"}
