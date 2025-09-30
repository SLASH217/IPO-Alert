"""Main IPO Alert application."""

import sys
from pathlib import Path
from typing import Optional, Dict

from .config import Config
from .database import IPODatabase
from .email_service import EmailService
from .logger import setup_logger, get_logger
from .scraper import IPOScraper


class IPOAlert:
    """Main IPO Alert application."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize IPO Alert application.

        Args:
            config_path: Optional path to configuration file
        """
        try:
            # Load configuration
            self.config = Config.from_env()
            self.config.validate()

            # Setup logging
            self.logger = setup_logger("ipo_alert", level=self.config.log_level)

            # Initialize components
            self.scraper = IPOScraper(self.config.source_url)
            self.email_service = EmailService(self.config)
            self.database = IPODatabase(self.config.notified_ipos_file)

            self.logger.info("IPO Alert application initialized successfully")

        except Exception as e:
            print(f"Failed to initialize IPO Alert: {e}")
            sys.exit(1)

    def run(self, dry_run: bool = False, force: bool = False) -> bool:
        """
        Run the IPO alert process.

        Args:
            dry_run: If True, don't send emails or save notifications
            force: If True, send notifications even if already sent

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Starting IPO alert process")

            # Test email connection first
            if not dry_run and not self.email_service.test_email_connection():
                self.logger.error("Email connection test failed. Aborting.")
                return False

            # Fetch and save HTML data
            if not self.scraper.fetch_and_save(self.config.data_path):
                self.logger.error("Failed to fetch IPO data. Aborting.")
                return False

            # Read and process HTML data
            html_content = self.scraper.read_html_file(self.config.data_path)
            ipo_data = self.scraper.extract_ipo_details(html_content)

            open_ipo = ipo_data.get("open_ipo")
            if not open_ipo:
                self.logger.info("No open IPOs found")
                return True

            self.logger.info(f"Found open IPO: {open_ipo.company_name}")

            # Check if already notified (unless forced)
            if not force and self.database.is_already_notified(open_ipo.company_name):
                self.logger.info(
                    f"Already notified about {open_ipo.company_name}. Skipping."
                )
                return True

            if dry_run:
                self.logger.info(
                    f"DRY RUN: Would send notification for {open_ipo.company_name}"
                )
                subject, body = self.email_service.prepare_ipo_notification(open_ipo)
                self.logger.info(f"Subject: {subject}")
                self.logger.info(
                    f"Recipients: {', '.join(self.config.recipient_emails)}"
                )
                return True

            # Send notifications
            results = self.email_service.send_ipo_notification(open_ipo)

            # Check if at least one email was sent successfully
            successful_sends = sum(results.values())
            if successful_sends > 0:
                # Save notification record
                if self.database.save_ipo_notification(open_ipo):
                    self.logger.info(
                        f"Successfully processed IPO notification for {open_ipo.company_name}"
                    )
                    return True
                else:
                    self.logger.warning("Failed to save notification record")
                    return False
            else:
                self.logger.error("Failed to send any notifications")
                return False

        except Exception as e:
            self.logger.error(f"Error during IPO alert process: {e}")
            return False

    def health_check(self) -> Dict[str, bool]:
        """
        Perform system health check.

        Returns:
            Dictionary with health check results
        """
        checks = {
            "config_valid": False,
            "email_connection": False,
            "source_accessible": False,
            "database_accessible": False,
        }

        try:
            # Check configuration
            self.config.validate()
            checks["config_valid"] = True

            # Check email connection
            checks["email_connection"] = self.email_service.test_email_connection()

            # Check source website accessibility
            checks["source_accessible"] = self.scraper.fetch_and_save(
                self.config.data_path.replace(".html", "_healthcheck.html")
            )

            # Check database accessibility
            test_data = self.database.load_history()
            checks["database_accessible"] = isinstance(test_data, dict)

        except Exception as e:
            self.logger.error(f"Health check error: {e}")

        return checks

    def get_stats(self) -> Dict:
        """
        Get application statistics.

        Returns:
            Dictionary containing application statistics
        """
        try:
            db_stats = self.database.get_stats()
            config_stats = {
                "recipient_count": len(self.config.recipient_emails),
                "source_url": self.config.source_url,
                "data_path": self.config.data_path,
            }

            return {"database": db_stats, "configuration": config_stats}

        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}

    def cleanup(self, days_to_keep: int = 30) -> bool:
        """
        Clean up old records.

        Args:
            days_to_keep: Number of days to keep records

        Returns:
            True if successful, False otherwise
        """
        try:
            removed_count = self.database.cleanup_old_records(days_to_keep)
            self.logger.info(f"Cleanup completed: removed {removed_count} records")
            return True
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return False
