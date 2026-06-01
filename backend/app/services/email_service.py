from email.message import EmailMessage
import os
import smtplib

from app.core.config import settings


class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST or os.getenv("EMAIL_HOST", "") or os.getenv("MAIL_HOST", "")
        self.port = int(settings.SMTP_PORT or os.getenv("EMAIL_PORT", 587) or os.getenv("MAIL_PORT", 587))
        self.username = settings.SMTP_USERNAME or os.getenv("EMAIL_USERNAME", "") or os.getenv("EMAIL_USER", "") or os.getenv("MAIL_USERNAME", "")
        self.password = settings.SMTP_PASSWORD or os.getenv("EMAIL_PASSWORD", "") or os.getenv("EMAIL_PASS", "") or os.getenv("MAIL_PASSWORD", "")
        self.from_email = settings.SMTP_FROM_EMAIL or os.getenv("EMAIL_FROM", "") or os.getenv("MAIL_FROM", "") or self.username
        self.from_name = settings.SMTP_FROM_NAME or os.getenv("EMAIL_FROM_NAME", "") or os.getenv("MAIL_FROM_NAME", "") or "TrustHire AI"
        raw_tls = os.getenv("EMAIL_USE_TLS", os.getenv("MAIL_USE_TLS", str(settings.SMTP_USE_TLS)))
        raw_ssl = os.getenv("SMTP_USE_SSL", os.getenv("EMAIL_USE_SSL", os.getenv("MAIL_USE_SSL", str(settings.SMTP_USE_SSL))))
        self.use_tls = str(raw_tls).lower() in {"1", "true", "yes", "on"}
        self.use_ssl = str(raw_ssl).lower() in {"1", "true", "yes", "on"} or self.port == 465

    def is_configured(self) -> bool:
        return bool(self.host and self.port and self.username and self.password and self.from_email)

    def send_password_reset_code(self, to_email: str, reset_code: str) -> None:
        if not self.is_configured():
            raise RuntimeError("SMTP is not configured. Required: SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL.")

        subject = "TrustHire AI password reset code"
        text_body = (
            "You requested a password reset for your TrustHire AI account.\n\n"
            f"Your reset code is: {reset_code}\n\n"
            "This code expires in 15 minutes. If you did not request this, you can ignore this email."
        )
        html_body = f"""
        <div style="font-family:Arial,sans-serif;background:#f8fafc;padding:24px;color:#0f172a">
          <div style="max-width:560px;margin:auto;background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden">
            <div style="background:#0f172a;color:#ffffff;padding:22px 26px">
              <h2 style="margin:0;font-size:22px">TrustHire AI</h2>
              <p style="margin:6px 0 0;color:#bfdbfe">Password reset verification</p>
            </div>
            <div style="padding:26px">
              <p style="font-size:15px;line-height:1.6">Use this code to reset your TrustHire AI password:</p>
              <div style="font-size:30px;font-weight:700;letter-spacing:8px;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;border-radius:8px;padding:16px;text-align:center">
                {reset_code}
              </div>
              <p style="font-size:14px;line-height:1.6;color:#475569;margin-top:20px">
                This code expires in 15 minutes. If you did not request this, you can ignore this email.
              </p>
            </div>
          </div>
        </div>
        """

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        message.set_content(text_body)
        message.add_alternative(html_body, subtype="html")

        smtp_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
        with smtp_class(self.host, self.port, timeout=20) as smtp:
            if self.use_tls and not self.use_ssl:
                smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(message)
