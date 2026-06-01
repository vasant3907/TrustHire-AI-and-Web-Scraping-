# Application constants
RISK_LEVELS = ["low", "medium", "high", "critical"]
SALARY_VALIDITY_OPTIONS = ["valid", "suspicious", "invalid"]
EMAIL_VALIDITY_OPTIONS = ["valid", "suspicious", "invalid"]

# Trust score thresholds
TRUST_SCORE_THRESHOLDS = {
    "safe": 80,      # >= 80
    "caution": 60,   # 60-79
    "risky": 40,     # 40-59
    "dangerous": 0   # < 40
}

# File upload limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "gif"]
ALLOWED_DOCUMENT_FORMATS = ["pdf", "txt", "docx"]
