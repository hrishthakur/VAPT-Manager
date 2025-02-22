import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the Secure Code Fix Recommendation System"""

    # OpenAI API Key
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found in environment variables")

    # JIRA Configuration
    JIRA_API_URL: Optional[str] = os.getenv("JIRA_API_URL")
    JIRA_USER: Optional[str] = os.getenv("JIRA_USER")
    JIRA_API_TOKEN: Optional[str] = os.getenv("JIRA_API_TOKEN")

    if not all([JIRA_API_URL, JIRA_USER, JIRA_API_TOKEN]):
        raise ValueError("Missing required JIRA configuration in environment variables")

    # Email Configuration
    EMAIL_USER: Optional[str] = os.getenv("EMAIL_USER")
    EMAIL_PASS: Optional[str] = os.getenv("EMAIL_PASS")
    SMTP_SERVER: str = (
        "smtp.gmail.com"  # Changed to Gmail SMTP server since email is Gmail
    )
    SMTP_PORT: int = 587

    if not all([EMAIL_USER, EMAIL_PASS]):
        raise ValueError("Missing email credentials in environment variables")

    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "security_fixes")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))

    # Database URL construction
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
