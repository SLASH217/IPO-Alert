"""Configuration management for IPO Alert application."""

import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Configuration class for IPO Alert application."""

    email_address: str
    app_password: str
    recipient_emails: List[str]
    source_url: str = "https://www.sharesansar.com"
    data_path: str = "data/share.html"
    notified_ipos_file: str = "data/ipo_history.json"
    log_level: str = "INFO"

    # Optional Resend configuration
    resend_api_key: str = None
    resend_from_email: str = None

    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        email_address = os.getenv("EMAIL_ADDRESS")
        app_password = os.getenv("APP_PASSWORD")

        if not email_address or not app_password:
            raise ValueError("EMAIL_ADDRESS and APP_PASSWORD must be set in environment variables")

        emails_str = os.getenv("RECIPIENT_EMAIL_LIST", "")
        recipient_emails = [email.strip() for email in emails_str.split(",") if email.strip()]

        if not recipient_emails:
            raise ValueError("RECIPIENT_EMAIL_LIST must be set in environment variables")

        return cls(
            email_address=email_address,
            app_password=app_password,
            recipient_emails=recipient_emails,
            source_url=os.getenv("SOURCE_URL", cls.source_url),
            data_path=os.getenv("DATA_PATH", cls.data_path),
            notified_ipos_file=os.getenv("NOTIFIED_IPOS_FILE", cls.notified_ipos_file),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            resend_api_key=os.getenv("RESEND_API_KEY"),
            resend_from_email=os.getenv("RESEND_FROM_EMAIL")
        )

    def validate(self) -> None:
        """Validate configuration parameters."""
        if not self.email_address or "@" not in self.email_address:
            raise ValueError("Invalid email address")

        if not self.app_password:
            raise ValueError("App password cannot be empty")

        if not self.recipient_emails:
            raise ValueError("At least one recipient email must be provided")

        for email in self.recipient_emails:
            if "@" not in email:
                raise ValueError(f"Invalid recipient email: {email}")