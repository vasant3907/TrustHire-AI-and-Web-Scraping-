"""
AI Service Module
Handles Gemini/Groq/OpenAI integration for job scam analysis.
"""

import json
import re
import base64
from typing import Any

import httpx

from app.core.config import settings


SUSPICIOUS_TERMS = {
    "registration fee",
    "security deposit",
    "processing fee",
    "training fee",
    "pay to apply",
    "whatsapp only",
    "telegram",
    "urgent hiring",
    "no interview",
    "work from home guaranteed",
    "refundable fee",
    "joining fee",
    "document charge",
    "upi payment",
    "paytm",
    "crypto",
    "gift card",
}


class AIService:
    def __init__(self):
        self.timeout = httpx.Timeout(35.0, connect=10.0)

    def analyze_job_description(self, jd: str, company_context: dict | None = None) -> dict:
        """
        Analyze a job description using Gemini/Groq/OpenAI when keys are configured.
        Falls back to local rules when APIs are unavailable.
        """
        company_context = company_context or {}
        prompt = self._build_prompt(jd, company_context)

        for provider in self._analysis_provider_order(jd, company_context):
            result = None
            if provider == "groq":
                result = self._analyze_with_groq(prompt)
            elif provider == "gemini":
                result = self._analyze_with_gemini(prompt)
            elif provider == "openai":
                result = self._analyze_with_openai(prompt)

            if result:
                return self._enforce_hard_red_flags(result, jd)

        return self._enforce_hard_red_flags(self._local_analysis(jd, company_context), jd)

    def validate_salary(self, salary: str, position: str) -> dict:
        text = f"{salary} {position}".lower()
        suspicious = bool(re.search(r"\b(\d{5,}|\d+\s*lpa)\b", text)) and any(
            word in text for word in ["easy", "guaranteed", "no interview", "urgent"]
        )
        return {
            "is_valid": not suspicious,
            "status": "suspicious" if suspicious else "valid",
            "reason": "High salary is paired with urgency or unrealistic promises." if suspicious else "No obvious salary red flags found.",
        }

    def validate_email(self, email: str, company_name: str = "") -> dict:
        domain_match = re.search(r"@([a-z0-9.-]+\.[a-z]{2,})", email.lower())
        if not domain_match:
            return {"is_valid": False, "status": "invalid", "reason": "No valid email domain found."}

        domain = domain_match.group(1)
        free_domain = domain in {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "proton.me"}
        company_token = re.sub(r"[^a-z0-9]", "", company_name.lower())
        domain_token = re.sub(r"[^a-z0-9]", "", domain.split(".")[0])
        matches_company = bool(company_token and (company_token in domain_token or domain_token in company_token))

        if free_domain:
            return {"is_valid": False, "status": "suspicious", "reason": "Recruiter is using a free email domain."}
        if company_name and not matches_company:
            return {"is_valid": False, "status": "suspicious", "reason": "Email domain does not clearly match the company name."}
        return {"is_valid": True, "status": "valid", "reason": "Email domain looks consistent."}

    def _build_prompt(self, jd: str, company_context: dict) -> str:
        return f"""
You are TrustHire AI, a job scam and company trust analyzer for freshers.
Analyze the job opportunity and return ONLY valid JSON.
Be specific and useful. Explain evidence from the job text, recruiter contact/domain, payment requests,
company web intelligence, review snippets, and uncertainty. If there is impersonation, payment before
interview, free email usage, or pressure tactics, make the risk clear.

JSON schema:
{{
  "trust_score": number between 0 and 100,
  "scam_probability": number between 0 and 100,
  "risk_level": "low" | "medium" | "high" | "critical",
  "suspicious_keywords": ["keyword"],
  "ai_summary": "detailed paragraph explaining evidence and confidence",
  "recommendation": "actionable safety advice with verification steps",
  "salary_validity": "valid" | "suspicious" | "invalid",
  "email_validity": "valid" | "suspicious" | "invalid"
}}

Job description:
{jd}

Company/web context:
{json.dumps(company_context, ensure_ascii=True)[:4000]}
""".strip()

    def _analyze_with_gemini(self, prompt: str) -> dict | None:
        model = settings.GEMINI_MODEL.replace("models/", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
        }
        try:
            response = httpx.post(
                url,
                params={"key": settings.GEMINI_API_KEY},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return self._normalize_ai_result(text, source="gemini")
        except Exception:
            return None

    def _analyze_with_openai(self, prompt: str) -> dict | None:
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Return only valid JSON for job scam analysis."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            return self._normalize_ai_result(text, source="openai")
        except Exception:
            return None

    def _analyze_with_groq(self, prompt: str) -> dict | None:
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "Return only valid JSON for job scam analysis."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.15,
            "response_format": {"type": "json_object"},
        }
        try:
            response = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            return self._normalize_ai_result(text, source="groq")
        except Exception:
            return None

    def _normalize_ai_result(self, raw: str | dict[str, Any], source: str) -> dict:
        data = raw if isinstance(raw, dict) else self._extract_json(raw)
        fallback = self._local_analysis(json.dumps(data), {})
        trust_score = float(data.get("trust_score", fallback["trust_score"]))
        trust_score = max(0.0, min(100.0, trust_score))
        risk_level = data.get("risk_level") or self._risk_from_score(trust_score)

        return {
            "trust_score": trust_score,
            "scam_probability": float(data.get("scam_probability", max(0.0, 100.0 - trust_score))),
            "risk_level": risk_level if risk_level in {"low", "medium", "high", "critical"} else self._risk_from_score(trust_score),
            "suspicious_keywords": list(data.get("suspicious_keywords") or []),
            "ai_summary": data.get("ai_summary") or f"AI analysis completed using {source}.",
            "recommendation": data.get("recommendation") or fallback["recommendation"],
            "salary_validity": data.get("salary_validity") or fallback["salary_validity"],
            "email_validity": data.get("email_validity") or fallback["email_validity"],
            "analysis_source": source,
        }

    def extract_text_from_image(self, image_bytes: bytes, mime_type: str) -> dict:
        if settings.GEMINI_API_KEY:
            result = self._ocr_with_gemini(image_bytes, mime_type)
            if result:
                return result
        return {
            "text": "",
            "source": "unavailable",
            "message": "OCR needs a working Gemini key for image text extraction.",
        }

    def summarize_reviews(self, company_name: str, reviews: list[dict]) -> str:
        if not reviews:
            return "No public review snippets were found from reachable pages."

        prompt = f"""
Summarize public review snippets for {company_name}.
Return 4 concise sentences covering employee sentiment, repeated warnings, positive signs, and trust impact.
Reviews:
{json.dumps(reviews[:8], ensure_ascii=True)}
""".strip()

        for provider in self._text_provider_order():
            text = None
            if provider == "groq":
                text = self._generate_text_with_groq(prompt)
            elif provider == "gemini":
                text = self._generate_text_with_gemini(prompt)
            elif provider == "openai":
                text = self._generate_text_with_openai(prompt)
            if text:
                return text

        snippets = [review.get("snippet") or review.get("title", "") for review in reviews[:4]]
        return " ".join(snippet for snippet in snippets if snippet) or "Review pages were found, but no readable snippets were available."

    def _ocr_with_gemini(self, image_bytes: bytes, mime_type: str) -> dict | None:
        model = settings.GEMINI_MODEL.replace("models/", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Extract all readable job, recruiter, company, salary, contact, URL, "
                                "and warning text from this screenshot. Return plain text only."
                            )
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64.b64encode(image_bytes).decode("ascii"),
                            }
                        },
                    ]
                }
            ]
        }
        try:
            response = httpx.post(url, params={"key": settings.GEMINI_API_KEY}, json=payload, timeout=self.timeout)
            response.raise_for_status()
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            return {"text": text, "source": "gemini_vision", "message": "OCR completed with Gemini vision."}
        except Exception:
            return None

    def _generate_text_with_gemini(self, prompt: str) -> str | None:
        model = settings.GEMINI_MODEL.replace("models/", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
        try:
            response = httpx.post(url, params={"key": settings.GEMINI_API_KEY}, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return None

    def _generate_text_with_openai(self, prompt: str) -> str | None:
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                json={
                    "model": settings.OPENAI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

    def _generate_text_with_groq(self, prompt: str) -> str | None:
        try:
            response = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

    def _analysis_provider_order(self, jd: str, company_context: dict) -> list[str]:
        providers = []
        text = jd.lower()
        needs_deep_reasoning = (
            len(jd) > 1500
            or any(term in text for term in SUSPICIOUS_TERMS)
            or bool(company_context.get("reviews"))
            or bool(company_context.get("public_mentions"))
        )

        if needs_deep_reasoning and settings.GROQ_API_KEY:
            providers.append("groq")
        if settings.GEMINI_API_KEY:
            providers.append("gemini")
        if not needs_deep_reasoning and settings.GROQ_API_KEY:
            providers.append("groq")
        if settings.OPENAI_API_KEY:
            providers.append("openai")
        return providers

    def _text_provider_order(self) -> list[str]:
        providers = []
        if settings.GROQ_API_KEY:
            providers.append("groq")
        if settings.GEMINI_API_KEY:
            providers.append("gemini")
        if settings.OPENAI_API_KEY:
            providers.append("openai")
        return providers

    def _extract_json(self, text: str) -> dict:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?|```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE).strip()
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            cleaned = match.group(0)
        return json.loads(cleaned)

    def _local_analysis(self, jd: str, company_context: dict) -> dict:
        text = jd.lower()
        matches = sorted(term for term in SUSPICIOUS_TERMS if term in text)
        free_email = bool(re.search(r"@(gmail|yahoo|outlook|hotmail|proton)\.(com|me)\b", text))
        salary = self.validate_salary(jd, "")
        company_found = bool(company_context.get("website") or company_context.get("search_results"))

        score = 85 - (len(matches) * 9) - (15 if free_email else 0) - (10 if salary["status"] == "suspicious" else 0)
        score += 8 if company_found else 0
        score = max(5, min(95, score))
        risk_level = self._risk_from_score(score)

        return {
            "trust_score": float(score),
            "scam_probability": float(100 - score),
            "risk_level": risk_level,
            "suspicious_keywords": matches,
            "ai_summary": f"Local fallback found {len(matches)} suspicious signal(s).",
            "recommendation": self._recommendation(risk_level),
            "salary_validity": salary["status"],
            "email_validity": "suspicious" if free_email else "valid",
            "analysis_source": "local_rules",
        }

    def _enforce_hard_red_flags(self, result: dict, jd: str) -> dict:
        text = jd.lower()
        payment_red_flag = any(
            term in text
            for term in [
                "security deposit",
                "registration fee",
                "processing fee",
                "training fee",
                "refundable fee",
                "joining fee",
                "upi",
                "paytm",
            ]
        )
        free_email = bool(re.search(r"@(gmail|yahoo|outlook|hotmail|proton)\.(com|me)\b", text))
        no_interview = "no interview" in text or "before interview" in text

        if payment_red_flag and (free_email or no_interview):
            result["trust_score"] = min(float(result.get("trust_score", 0)), 10.0)
            result["scam_probability"] = max(float(result.get("scam_probability", 0)), 95.0)
            result["risk_level"] = "critical"
            result["recommendation"] = (
                "Do not proceed or pay any amount. Verify only through the official company careers page, "
                "official domain email, and a documented interview process. Treat payment requests before hiring as a scam."
            )
        elif payment_red_flag:
            result["trust_score"] = min(float(result.get("trust_score", 0)), 35.0)
            result["scam_probability"] = max(float(result.get("scam_probability", 0)), 80.0)
            result["risk_level"] = "high"
        return result

    def _risk_from_score(self, score: float) -> str:
        if score >= 80:
            return "low"
        if score >= 60:
            return "medium"
        if score >= 40:
            return "high"
        return "critical"

    def _recommendation(self, risk_level: str) -> str:
        if risk_level == "low":
            return "Looks reasonable. Still verify the company domain, recruiter identity, and offer letter."
        if risk_level == "medium":
            return "Proceed carefully. Ask for official email communication and verify the role on company channels."
        if risk_level == "high":
            return "High-risk signals found. Do not pay fees or share sensitive documents until verified."
        return "Avoid this opportunity unless it can be verified through official company channels."
