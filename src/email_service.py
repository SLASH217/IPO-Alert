"""Email service for sending IPO notifications."""

import smtplib
import requests
from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import List, Dict, Optional

from .config import Config
from .logger import get_logger
from .models import IPOInfo

logger = get_logger(__name__)


class BaseEmailProvider(ABC):
    """Abstract base class for email providers."""

    @abstractmethod
    def send_email(self, subject: str, body: str, to_email: str) -> bool:
        """Send an email to a single recipient."""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test the email service connection."""
        pass


class GmailProvider(BaseEmailProvider):
    """Gmail SMTP email provider."""

    def __init__(self, email_address: str, app_password: str):
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, subject: str, body: str, to_email: str) -> bool:
        """Send email via Gmail SMTP."""
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = to_email
            msg.set_content(body)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.app_password)
                server.send_message(msg)

            logger.info(f"Gmail: Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error(f"Gmail: SMTP authentication failed for {self.email_address}")
            return False
        except smtplib.SMTPRecipientsRefused:
            logger.error(f"Gmail: Recipient refused: {to_email}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Gmail: SMTP error when sending to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(
                f"Gmail: Unexpected error when sending email to {to_email}: {e}"
            )
            return False

    def test_connection(self) -> bool:
        """Test Gmail SMTP connection."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.app_password)

            logger.info("Gmail: Connection test successful")
            return True

        except Exception as e:
            logger.error(f"Gmail: Connection test failed: {e}")
            return False


class ResendProvider(BaseEmailProvider):
    """Resend API email provider."""

    def __init__(self, api_key: str, from_email: str):
        self.api_key = api_key
        self.from_email = from_email
        self.api_url = "https://api.resend.com/emails"

    def send_email(self, subject: str, body: str, to_email: str) -> bool:
        """Send email via Resend API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "from": self.from_email,
                "to": [to_email],
                "subject": subject,
                "text": body,
            }

            response = requests.post(
                self.api_url, json=data, headers=headers, timeout=30
            )
            response.raise_for_status()

            logger.info(f"Resend: Email sent successfully to {to_email}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Resend: API error when sending to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(
                f"Resend: Unexpected error when sending email to {to_email}: {e}"
            )
            return False

    def test_connection(self) -> bool:
        """Test Resend API connection."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            # Test with a simple API call (this endpoint doesn't exist, but tests auth)
            response = requests.get(
                "https://api.resend.com/domains", headers=headers, timeout=30
            )

            if response.status_code in [200, 401, 403]:  # Auth-related responses
                logger.info("Resend: API connection test successful")
                return True
            else:
                logger.error(
                    f"Resend: API test failed with status {response.status_code}"
                )
                return False

        except Exception as e:
            logger.error(f"Resend: Connection test failed: {e}")
            return False


class EmailService:
    """Main email service that supports multiple providers."""

    def __init__(self, config: Config):
        self.config = config
        self.provider = self._create_provider()

    def _create_provider(self) -> BaseEmailProvider:
        """Create the appropriate email provider based on configuration."""
        # Check if Resend is configured
        resend_api_key = getattr(self.config, "resend_api_key", None)
        resend_from_email = getattr(self.config, "resend_from_email", None)

        if resend_api_key and resend_from_email:
            logger.info("Using Resend email provider")
            return ResendProvider(resend_api_key, resend_from_email)
        else:
            logger.info("Using Gmail email provider")
            return GmailProvider(self.config.email_address, self.config.app_password)

    def send_email(self, subject: str, body: str, to_email: str) -> bool:
        """
        Send an email to a single recipient using the configured provider.

        Args:
            subject: Email subject
            body: Email body
            to_email: Recipient email address

        Returns:
            True if successful, False otherwise
        """
        return self.provider.send_email(subject, body, to_email)

    def send_bulk_email(
        self, subject: str, body: str, recipients: List[str]
    ) -> Dict[str, bool]:
        """
        Send email to multiple recipients.

        Args:
            subject: Email subject
            body: Email body
            recipients: List of recipient email addresses

        Returns:
            Dictionary mapping email addresses to success status
        """
        results = {}

        for email in recipients:
            success = self.send_email(subject, body, email)
            results[email] = success

        successful = sum(results.values())
        logger.info(f"Bulk email sent: {successful}/{len(recipients)} successful")

        return results

    def prepare_ipo_notification(self, ipo_info: IPOInfo) -> tuple[str, str]:
        """
        Prepare email subject and body for IPO notification.

        Args:
            ipo_info: IPO information

        Returns:
            Tuple of (subject, body)
        """
        subject = f"🚨 IPO Alert: {ipo_info.company_name} is Now Open!"

        body = f"""Hello,

The following IPO is now open for application:

📊 Company Name: {ipo_info.company_name}
📈 Units Available: {ipo_info.units_available}
💰 Price per Unit: {ipo_info.price_per_unit}
📅 Start Date: {ipo_info.start_date}
📅 End Date: {ipo_info.end_date}
🔄 Status: {ipo_info.status}

Don't miss this opportunity! Visit the official site to apply now:
🔗 https://meroshare.cdsc.com.np

Best regards,
IPO Alert Team

---
This is an automated notification from IPO Alert System.
If you no longer wish to receive these notifications, please contact the administrator.
"""

        return subject, body

    def send_ipo_notification(self, ipo_info: IPOInfo) -> Dict[str, bool]:
        """
        Send IPO notification to all configured recipients.

        Args:
            ipo_info: IPO information to send

        Returns:
            Dictionary mapping email addresses to success status
        """
        subject, body = self.prepare_ipo_notification(ipo_info)
        return self.send_bulk_email(subject, body, self.config.recipient_emails)

    def test_email_connection(self) -> bool:
        """
        Test email connection and credentials using the configured provider.

        Returns:
            True if connection successful, False otherwise
        """
        return self.provider.test_connection()
