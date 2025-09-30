"""Logging configuration for IPO Alert application."""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    name: str, log_file: str = "logs/ipo_alert.log", level: str = "INFO"
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level

    Returns:
        Configured logger instance
    """
    # Ensure logs directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5  # 1MB
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
