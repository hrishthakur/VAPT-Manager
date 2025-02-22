from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging
import smtplib

logger = logging.getLogger(__name__)


class EmailNotifier:
    def __init__(self):
        self.config = Config()
        self.smtp_server = self.config.SMTP_SERVER
        self.smtp_port = self.config.SMTP_PORT
        self.email_user = self.config.EMAIL_USER
        self.email_pass = self.config.EMAIL_PASS

    def send_email(self, vulnerability, fixes, jira_ticket_id=None):
        """Sends an HTML-formatted email notification"""
        try:
            recipients = ["security_team@example.com", "dev_team@example.com"]
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Security Alert: {vulnerability['name']}"
            msg["From"] = self.email_user

            html_content = f"""
            <html>
              <body>
                <h2>Security Vulnerability Alert</h2>
                <h3>Issue: {vulnerability["name"]}</h3>
                <p><strong>Description:</strong> {vulnerability["description"]}</p>
                <p><strong>Impact:</strong> {vulnerability["impact"]}</p>
                <p><strong>Technology Stack:</strong> {vulnerability["tech_stack"]}</p>
                
                <h3>Recommended Fixes:</h3>
                <pre>{fixes}</pre>
                
                {f"<p><strong>Jira Ticket:</strong> {jira_ticket_id}</p>" if jira_ticket_id else ""}
              </body>
            </html>
            """

            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                for recipient in recipients:
                    msg["To"] = recipient
                    server.send_message(msg)

            logger.info(
                f"Email notification sent for vulnerability: {vulnerability['name']}"
            )

        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            raise
