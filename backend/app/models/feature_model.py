from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from app.core.database import Base


class CommunityScamReport(Base):
    __tablename__ = "community_scam_reports"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    recruiter_email = Column(String(255), nullable=True)
    platform = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    evidence_url = Column(String(500), nullable=True)
    status = Column(String(50), default="submitted")
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WatchlistEntry(Base):
    __tablename__ = "watchlist_entries"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    recruiter_email = Column(String(255), nullable=True)
    reason = Column(Text, nullable=False)
    severity = Column(String(50), default="medium")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserReportNote(Base):
    __tablename__ = "user_report_notes"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("analysis_reports.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text, nullable=True)
    bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("analysis_reports.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel = Column(String(50), default="in_app")
    message = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(100), unique=True, index=True, nullable=False)
    used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
