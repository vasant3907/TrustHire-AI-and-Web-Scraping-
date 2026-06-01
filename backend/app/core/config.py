import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_TITLE: str = "TrustHire AI API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered job opportunity analysis and scam detection"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"]
    
    # AI & External Services
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    ADMIN_EMAILS: str = ""

    # Email / SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "TrustHire AI"
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
