"""Data models for IPO Alert application."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class IPOInfo:
    """IPO information data model."""

    company_name: str
    units_available: str
    price_per_unit: str
    start_date: str
    end_date: str
    status: str

    def __post_init__(self):
        """Validate IPO data after initialization."""
        if not self.company_name.strip():
            raise ValueError("Company name cannot be empty")

        if not self.status.strip():
            raise ValueError("Status cannot be empty")

    @property
    def is_open(self) -> bool:
        """Check if IPO is currently open."""
        return self.status.lower().strip() == "open"

    def to_dict(self) -> Dict[str, Any]:
        """Convert IPO info to dictionary."""
        return {
            "company_name": self.company_name,
            "units_available": self.units_available,
            "price_per_unit": self.price_per_unit,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
        }

    @classmethod
    def from_row_data(cls, row_data: list, headings: Dict[str, int]) -> "IPOInfo":
        """Create IPO info from table row data and headings mapping."""
        try:
            return cls(
                company_name=row_data[headings.get("Company Name", 2)],
                units_available=row_data[headings.get("Units", 3)],
                price_per_unit=row_data[headings.get("Price", 4)],
                start_date=row_data[headings.get("Open Date", 5)],
                end_date=row_data[headings.get("Close Date", 6)],
                status=row_data[headings.get("Status", 1)],
            )
        except (IndexError, KeyError) as e:
            raise ValueError(f"Invalid row data or headings mapping: {e}")


@dataclass
class NotificationRecord:
    """Record of sent notifications."""

    company_name: str
    notified_at: datetime
    ipo_data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert notification record to dictionary."""
        return {
            "company_name": self.company_name,
            "notified_at": self.notified_at.isoformat(),
            "ipo_data": self.ipo_data,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotificationRecord":
        """Create notification record from dictionary."""
        return cls(
            company_name=data["company_name"],
            notified_at=datetime.fromisoformat(data["notified_at"]),
            ipo_data=data["ipo_data"],
        )
