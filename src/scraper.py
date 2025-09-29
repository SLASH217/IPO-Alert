"""Web scraping functionality for IPO data."""

import os
import re
import time
from functools import wraps
from pathlib import Path
from typing import Optional, Dict, List

import requests
from bs4 import BeautifulSoup

from .logger import get_logger
from .models import IPOInfo

logger = get_logger(__name__)


class IPOExtractionError(Exception):
    """Custom exception for IPO extraction errors."""
    pass


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator for network operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


class IPOScraper:
    """IPO data scraper."""

    def __init__(self, source_url: str = "https://www.sharesansar.com"):
        self.source_url = source_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    @retry(max_attempts=3, delay=2.0)
    def fetch_and_save(self, file_path: str) -> bool:
        """
        Fetch website content and save it locally.

        Args:
            file_path: Path to save the HTML content

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Fetching data from {self.source_url}")
            response = self.session.get(self.source_url, timeout=30)
            response.raise_for_status()

            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            logger.info(f"Data saved successfully to {file_path}")
            return True

        except requests.exceptions.Timeout:
            logger.error(f"Timeout error when fetching {self.source_url}")
            return False
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error when fetching {self.source_url}")
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when fetching {self.source_url}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error when fetching data: {e}")
            return False

    def read_html_file(self, file_path: str) -> str:
        """
        Read HTML content from file.

        Args:
            file_path: Path to HTML file

        Returns:
            HTML content as string
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            logger.debug(f"Successfully read {len(content)} characters from {file_path}")
            return content
        except FileNotFoundError:
            logger.error(f"HTML file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading HTML file {file_path}: {e}")
            raise

    def extract_ipo_details(self, html_content: str) -> Dict:
        """
        Extract IPO details from HTML content.

        Args:
            html_content: HTML content to parse

        Returns:
            Dictionary containing headings, data, and open IPO info
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Find IPO section
            ipo_div = self._safe_find(soup, "find", id="eipo")
            if not ipo_div:
                raise IPOExtractionError("IPO section not found on the page")

            # Find table body
            table_body = self._safe_find(ipo_div, "find", "tbody")
            if not table_body:
                raise IPOExtractionError("IPO table body not found")

            # Extract headings and data
            headings = self._extract_table_headings(ipo_div)
            data = self._extract_table_data(table_body)
            open_ipo = self._get_open_ipo(data, headings)

            logger.info(f"Extracted {len(data)} IPO entries from HTML")
            return {
                "headings": list(headings.keys()),
                "data": data,
                "open_ipo": open_ipo
            }

        except Exception as e:
            logger.error(f"Error extracting IPO details: {e}")
            raise IPOExtractionError(f"Failed to extract IPO details: {e}")

    def _safe_find(self, obj, method: str, *args, **kwargs):
        """Safely execute BeautifulSoup find methods."""
        try:
            return getattr(obj, method)(*args, **kwargs)
        except AttributeError:
            return None

    def _extract_table_headings(self, ipo_div) -> Dict[str, int]:
        """Extract table headings and map them to column indices."""
        headings = []
        th_elements = self._safe_find(ipo_div, "find_all", "th") or []

        for th in th_elements:
            heading_text = self._clean_text(th.text)
            headings.append(heading_text)

        if not headings:
            raise IPOExtractionError("No table headings found")

        heading_map = {heading: index for index, heading in enumerate(headings)}
        logger.debug(f"Found headings: {list(heading_map.keys())}")
        return heading_map

    def _extract_table_data(self, table_body) -> List[List[str]]:
        """Extract table data from tbody element."""
        data = []
        rows = self._safe_find(table_body, "find_all", "tr") or []

        for row in rows:
            cols = self._safe_find(row, "find_all", "td") or []
            row_data = [self._clean_text(col.text) for col in cols]
            if row_data:  # Only add non-empty rows
                data.append(row_data)

        return data

    def _get_open_ipo(self, data: List[List[str]], headings: Dict[str, int]) -> Optional[IPOInfo]:
        """Find and return the first open IPO."""
        status_col = headings.get("Status")
        if status_col is None:
            logger.warning("Status column not found in headings")
            return None

        for row in data:
            if len(row) > status_col and row[status_col].strip().lower() == "open":
                try:
                    ipo_info = IPOInfo.from_row_data(row, headings)
                    logger.info(f"Found open IPO: {ipo_info.company_name}")
                    return ipo_info
                except ValueError as e:
                    logger.warning(f"Error creating IPO info from row: {e}")
                    continue

        logger.info("No open IPOs found")
        return None

    def _clean_text(self, text: str) -> str:
        """Clean text by removing newlines, tabs, and excess spaces."""
        if not text:
            return ""

        # Replace newlines and tabs with spaces
        cleaned = text.replace("\n", " ").replace("\t", " ")
        # Remove excess whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned