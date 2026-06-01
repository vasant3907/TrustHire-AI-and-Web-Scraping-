from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.dependencies.auth_dependency import get_current_user
from app.models.feature_model import PasswordResetToken
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import ForgotPassword, PasswordChange, PasswordResetConfirm, UserCreate, UserResponse, UserLogin, UserUpdate
from app.schemas.auth_schema import Token
from app.core.config import settings
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def is_admin_user(user) -> bool:
    admin_emails = {email.strip().lower() for email in settings.ADMIN_EMAILS.split(",") if email.strip()}
    return user.id == 1 or user.email.lower() in admin_emails


def make_user_token_response(user: User) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_admin": is_admin_user(user)
    }


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user_repo = UserRepository(db)
    
    # Check if user already exists
    existing_user = user_repo.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = user_repo.create_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )
    
    return user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user_repo = UserRepository(db)
    
    # Verify credentials
    user = user_repo.verify_user_credentials(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return make_user_token_response(user)


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Return current user profile"""
    return current_user


@router.put("/me", response_model=Token)
def update_my_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user's name/email and return a fresh token"""
    user_repo = UserRepository(db)
    clean_name = payload.name.strip()
    if not clean_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")

    clean_email = str(payload.email)
    existing_user = user_repo.get_user_by_email(clean_email)
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    updated_user = user_repo.update_user(current_user, clean_name, clean_email)
    return make_user_token_response(updated_user)


@router.post("/change-password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Change current user's password after verifying the old password"""
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 8 characters")
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    UserRepository(db).update_password(current_user, payload.new_password)
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPassword, db: Session = Depends(get_db)):
    """Create a short-lived reset code and send it to the user's email."""
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(str(payload.email))
    if user:
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used == False,  # noqa: E712
        ).update({"used": True})
        token = f"{secrets.randbelow(1000000):06d}"
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        )
        db.add(reset_token)
        db.commit()

        try:
            EmailService().send_password_reset_code(user.email, token)
        except Exception as exc:
            reset_token.used = True
            db.commit()
            reason = str(exc).replace(settings.SMTP_PASSWORD, "***") if settings.SMTP_PASSWORD else str(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to send reset email. SMTP error: {type(exc).__name__}: {reason}",
            )

        return {
            "message": "If this email exists, a reset code has been sent.",
            "delivery": "email",
        }

    return {"message": "If this email exists, a reset code has been sent.", "delivery": "email"}


@router.post("/reset-password")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password with a valid short-lived code."""
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 8 characters")

    reset_token = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == payload.reset_token.strip(),
            PasswordResetToken.used == False,  # noqa: E712
        )
        .order_by(PasswordResetToken.created_at.desc())
        .first()
    )
    if not reset_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or already used reset code")

    expires_at = reset_token.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        reset_token.used = True
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset code expired")

    user = UserRepository(db).get_user_by_id(reset_token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    UserRepository(db).update_password(user, payload.new_password)
    reset_token.used = True
    db.commit()

    return {"message": "Password reset successfully. You can sign in now."}
