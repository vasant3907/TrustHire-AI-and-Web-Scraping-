import re

import dns.resolver


FREE_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "proton.me"}


class VerificationService:
    def verify_domain(self, email: str, company_name: str = "") -> dict:
        match = re.search(r"@([a-z0-9.-]+\.[a-z]{2,})", (email or "").lower())
        if not match:
            return {"status": "invalid", "domain": None, "mx_found": False, "matches_company": False, "reason": "No valid email domain found."}

        domain = match.group(1)
        mx_found = self._has_mx(domain)
        company_token = re.sub(r"[^a-z0-9]", "", company_name.lower())
        domain_token = re.sub(r"[^a-z0-9]", "", domain.split(".")[0])
        matches_company = bool(company_token and (company_token in domain_token or domain_token in company_token))

        if domain in FREE_EMAIL_DOMAINS:
            status = "suspicious"
            reason = "Recruiter is using a free email provider instead of an official company domain."
        elif not mx_found:
            status = "invalid"
            reason = "Email domain has no reachable MX record."
        elif company_name and not matches_company:
            status = "suspicious"
            reason = "Email domain does not clearly match the company name."
        else:
            status = "valid"
            reason = "Domain has mail records and appears consistent with the company."

        return {
            "status": status,
            "domain": domain,
            "mx_found": mx_found,
            "matches_company": matches_company,
            "reason": reason,
        }

    def _has_mx(self, domain: str) -> bool:
        try:
            return bool(dns.resolver.resolve(domain, "MX", lifetime=4))
        except Exception:
            return False
