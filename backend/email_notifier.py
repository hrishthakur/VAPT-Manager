import smtplib
import os

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(vulnerability, fixes):
    """Sends an email notification about the vulnerability and fix recommendations"""
    recipients = ["security_team@example.com", "dev_team@example.com"]
    subject = f"Security Alert: {vulnerability['name']}"
    body = f"""
    Issue: {vulnerability['description']}
    Impact: {vulnerability['impact']}
    Recommended Fixes:
    {fixes}
    """

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        for recipient in recipients:
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_USER, recipient, message)
