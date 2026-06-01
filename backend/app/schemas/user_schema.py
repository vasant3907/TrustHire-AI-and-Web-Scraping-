from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    reset_token: str
    new_password: str
