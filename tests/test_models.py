"""Tests for IPO data models."""

import pytest
from datetime import datetime
from src.models import IPOInfo, NotificationRecord


class TestIPOInfo:
    """Test cases for IPOInfo model."""

    def test_ipo_info_creation(self):
        """Test IPOInfo creation with valid data."""
        ipo = IPOInfo(
            company_name="Test Company",
            units_available="1,000,000",
            price_per_unit="NPR 100",
            start_date="2025-01-15",
            end_date="2025-01-25",
            status="open"
        )

        assert ipo.company_name == "Test Company"
        assert ipo.is_open is True

    def test_ipo_info_empty_company_name(self):
        """Test IPOInfo validation with empty company name."""
        with pytest.raises(ValueError, match="Company name cannot be empty"):
            IPOInfo(
                company_name="",
                units_available="1,000,000",
                price_per_unit="NPR 100",
                start_date="2025-01-15",
                end_date="2025-01-25",
                status="open"
            )

    def test_ipo_info_status_check(self):
        """Test IPO status checking."""
        ipo_open = IPOInfo(
            company_name="Test Company",
            units_available="1,000,000",
            price_per_unit="NPR 100",
            start_date="2025-01-15",
            end_date="2025-01-25",
            status="open"
        )

        ipo_closed = IPOInfo(
            company_name="Test Company",
            units_available="1,000,000",
            price_per_unit="NPR 100",
            start_date="2025-01-15",
            end_date="2025-01-25",
            status="closed"
        )

        assert ipo_open.is_open is True
        assert ipo_closed.is_open is False

    def test_ipo_info_to_dict(self):
        """Test IPOInfo to dictionary conversion."""
        ipo = IPOInfo(
            company_name="Test Company",
            units_available="1,000,000",
            price_per_unit="NPR 100",
            start_date="2025-01-15",
            end_date="2025-01-25",
            status="open"
        )

        result = ipo.to_dict()
        expected = {
            "company_name": "Test Company",
            "units_available": "1,000,000",
            "price_per_unit": "NPR 100",
            "start_date": "2025-01-15",
            "end_date": "2025-01-25",
            "status": "open"
        }

        assert result == expected

    def test_ipo_info_from_row_data(self):
        """Test IPOInfo creation from row data."""
        row_data = ["1", "open", "Test Company", "1,000,000", "NPR 100", "2025-01-15", "2025-01-25"]
        headings = {
            "Company Name": 2,
            "Units": 3,
            "Price": 4,
            "Open Date": 5,
            "Close Date": 6,
            "Status": 1
        }

        ipo = IPOInfo.from_row_data(row_data, headings)

        assert ipo.company_name == "Test Company"
        assert ipo.status == "open"
        assert ipo.is_open is True


class TestNotificationRecord:
    """Test cases for NotificationRecord model."""

    def test_notification_record_creation(self):
        """Test NotificationRecord creation."""
        now = datetime.now()
        ipo_data = {"company_name": "Test Company", "status": "open"}

        record = NotificationRecord(
            company_name="Test Company",
            notified_at=now,
            ipo_data=ipo_data
        )

        assert record.company_name == "Test Company"
        assert record.notified_at == now
        assert record.ipo_data == ipo_data

    def test_notification_record_to_dict(self):
        """Test NotificationRecord to dictionary conversion."""
        now = datetime.now()
        ipo_data = {"company_name": "Test Company", "status": "open"}

        record = NotificationRecord(
            company_name="Test Company",
            notified_at=now,
            ipo_data=ipo_data
        )

        result = record.to_dict()

        assert result["company_name"] == "Test Company"
        assert result["notified_at"] == now.isoformat()
        assert result["ipo_data"] == ipo_data

    def test_notification_record_from_dict(self):
        """Test NotificationRecord creation from dictionary."""
        now = datetime.now()
        data = {
            "company_name": "Test Company",
            "notified_at": now.isoformat(),
            "ipo_data": {"company_name": "Test Company", "status": "open"}
        }

        record = NotificationRecord.from_dict(data)

        assert record.company_name == "Test Company"
        assert record.notified_at == now.replace(microsecond=0)  # ISO format loses microseconds
        assert record.ipo_data == data["ipo_data"]