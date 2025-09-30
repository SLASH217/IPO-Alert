"""Database management for IPO notification records."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .logger import get_logger
from .models import IPOInfo, NotificationRecord

logger = get_logger(__name__)


class IPODatabase:
    """Database for managing IPO notification records."""

    def __init__(self, db_path: str = "data/ipo_history.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure database file exists
        if not self.db_path.exists():
            self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize empty database file."""
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
            logger.info(f"Initialized new database at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def save_ipo_notification(self, ipo_info: IPOInfo) -> bool:
        """
        Save IPO notification record.

        Args:
            ipo_info: IPO information that was notified

        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.load_history()

            notification_record = NotificationRecord(
                company_name=ipo_info.company_name,
                notified_at=datetime.now(),
                ipo_data=ipo_info.to_dict(),
            )

            data[ipo_info.company_name] = notification_record.to_dict()

            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved notification record for {ipo_info.company_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to save notification record: {e}")
            return False

    def is_already_notified(self, company_name: str) -> bool:
        """
        Check if IPO was already notified.

        Args:
            company_name: Name of the company to check

        Returns:
            True if already notified, False otherwise
        """
        try:
            data = self.load_history()
            is_notified = company_name in data

            if is_notified:
                record = data[company_name]
                logger.info(
                    f"IPO {company_name} was already notified at {record.get('notified_at')}"
                )

            return is_notified

        except Exception as e:
            logger.error(f"Error checking notification status: {e}")
            return False

    def load_history(self) -> Dict:
        """
        Load notification history from database.

        Returns:
            Dictionary containing notification history
        """
        try:
            if not self.db_path.exists():
                return {}

            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in database file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return {}

    def get_notification_records(self) -> List[NotificationRecord]:
        """
        Get all notification records.

        Returns:
            List of notification records
        """
        try:
            data = self.load_history()
            records = []

            for record_data in data.values():
                try:
                    record = NotificationRecord.from_dict(record_data)
                    records.append(record)
                except Exception as e:
                    logger.warning(f"Skipping invalid record: {e}")
                    continue

            return records

        except Exception as e:
            logger.error(f"Error getting notification records: {e}")
            return []

    def cleanup_old_records(self, days_to_keep: int = 30) -> int:
        """
        Remove old notification records.

        Args:
            days_to_keep: Number of days to keep records

        Returns:
            Number of records removed
        """
        try:
            data = self.load_history()
            cutoff_date = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_to_keep)

            original_count = len(data)

            # Filter out old records
            filtered_data = {}
            for company, record_data in data.items():
                try:
                    notified_at = datetime.fromisoformat(record_data["notified_at"])
                    if notified_at >= cutoff_date:
                        filtered_data[company] = record_data
                except Exception as e:
                    logger.warning(f"Invalid date format in record for {company}: {e}")
                    # Keep records with invalid dates
                    filtered_data[company] = record_data

            # Save cleaned data
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(filtered_data, f, indent=2, ensure_ascii=False)

            removed_count = original_count - len(filtered_data)
            logger.info(f"Cleanup completed: removed {removed_count} old records")

            return removed_count

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return 0

    def get_stats(self) -> Dict:
        """
        Get database statistics.

        Returns:
            Dictionary containing database statistics
        """
        try:
            records = self.get_notification_records()

            if not records:
                return {
                    "total_notifications": 0,
                    "first_notification": None,
                    "last_notification": None,
                    "database_size_kb": 0,
                }

            dates = [record.notified_at for record in records]
            file_size = self.db_path.stat().st_size / 1024  # KB

            return {
                "total_notifications": len(records),
                "first_notification": min(dates).isoformat(),
                "last_notification": max(dates).isoformat(),
                "database_size_kb": round(file_size, 2),
            }

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
