#!/usr/bin/env python3
"""
IPO Alert - Automated IPO Notification System

This is the main entry point for the IPO Alert application.
It monitors Sharesansar.com for new IPO openings and sends email notifications.

Usage:
    python main.py              # Run the IPO alert process
    python cli.py run           # Alternative using CLI
    python cli.py --help        # See all available commands

Author: Prashanna Dahal
GitHub: SLASH217
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.main_app import IPOAlert
    from src.logger import setup_logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main entry point."""
    logger = setup_logger("main")

    try:
        logger.info("Starting IPO Alert application")

        # Initialize and run the application
        app = IPOAlert()
        success = app.run()

        if success:
            logger.info("IPO Alert completed successfully")
            print("✅ IPO Alert process completed successfully!")
        else:
            logger.error("IPO Alert process failed")
            print("❌ IPO Alert process failed. Check logs for details.")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\n⚠️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        print("Check logs for detailed error information.")
        sys.exit(1)


if __name__ == "__main__":
    main()