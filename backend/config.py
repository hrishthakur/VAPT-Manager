import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the Secure Code Fix Recommendation System"""

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # JIRA Configuration
    JIRA_API_URL = os.getenv("JIRA_API_URL")
    JIRA_USER = os.getenv("JIRA_USER")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

    # Outlook SMTP Configuration
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    SMTP_SERVER = "smtp.office365.com"
    SMTP_PORT = 587

    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "security_fixes")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
