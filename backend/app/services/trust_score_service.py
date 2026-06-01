"""
Trust Score Service Module
Calculates overall trust score based on various factors
"""

class TrustScoreService:
    def __init__(self):
        self.weights = {
            "company_presence": 0.25,
            "salary_validity": 0.25,
            "email_validity": 0.2,
            "suspicious_keywords": 0.2,
            "reviews": 0.1
        }

    def calculate_trust_score(self, factors: dict) -> dict:
        """
        Calculate trust score from various factors
        
        factors: {
            "company_presence_score": float (0-100),
            "salary_validity": bool,
            "email_validity": bool,
            "suspicious_keywords_count": int,
            "company_reviews": dict
        }
        
        Returns:
            {
                "trust_score": float (0-100),
                "risk_level": "low|medium|high|critical",
                "explanation": str
            }
        """
        # TODO: Implement trust score calculation
        return {
            "trust_score": 50.0,
            "risk_level": "medium",
            "explanation": "Calculation pending"
        }

    def determine_risk_level(self, trust_score: float) -> str:
        """Determine risk level from trust score"""
        if trust_score >= 80:
            return "low"
        elif trust_score >= 60:
            return "medium"
        elif trust_score >= 40:
            return "high"
        else:
            return "critical"
