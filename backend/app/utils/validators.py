import re
import logging

logger = logging.getLogger(__name__)

SUSPICIOUS_KEYWORDS = [
    "pay training fee",
    "immediate joining",
    "guaranteed placement",
    "no interview required",
    "work from home scam",
    "no experience required",
    "guaranteed salary",
    "risk free",
    "click here",
    "confirm payment"
]

def check_suspicious_keywords(text: str) -> dict:
    """
    Check for suspicious keywords in job description
    """
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return {
        "suspicious_keywords": found_keywords,
        "risk_score": len(found_keywords) * 10  # 10 points per keyword
    }

def extract_email_domain(email: str) -> str:
    """Extract domain from email"""
    if "@" in email:
        return email.split("@")[1].lower()
    return None

def extract_salary_range(text: str) -> dict:
    """Extract salary information from text"""
    # Simple regex to find salary patterns
    salary_pattern = r'₹?\s*(\d+(?:,\d+)*)\s*(?:to|[-–])\s*(\d+(?:,\d+)*)|₹?\s*(\d+(?:,\d+)*)\s*(?:per|\/)'
    matches = re.finditer(salary_pattern, text)
    
    salaries = []
    for match in matches:
        salaries.append(match.group())
    
    return {"salary_mentions": salaries}
