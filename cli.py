"""Command line interface for IPO Alert application."""

import argparse
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.main_app import IPOAlert
from src.logger import setup_logger

logger = setup_logger("cli")


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="IPO Alert Automation - Monitor and notify about IPO openings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py run                    # Run IPO alert process
  python cli.py run --dry-run         # Run without sending emails
  python cli.py run --force           # Force notification even if already sent
  python cli.py health                # Check system health
  python cli.py stats                 # Show statistics
  python cli.py cleanup               # Clean up old records
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run IPO alert process")
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without sending emails or saving notifications"
    )
    run_parser.add_argument(
        "--force",
        action="store_true",
        help="Force notification even if already sent"
    )

    # Health check command
    subparsers.add_parser("health", help="Perform system health check")

    # Stats command
    subparsers.add_parser("stats", help="Show application statistics")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old records")
    cleanup_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to keep records (default: 30)"
    )

    return parser


def handle_run_command(args) -> int:
    """Handle the run command."""
    try:
        app = IPOAlert()
        success = app.run(dry_run=args.dry_run, force=args.force)

        if success:
            logger.info("IPO alert process completed successfully")
            return 0
        else:
            logger.error("IPO alert process failed")
            return 1

    except Exception as e:
        logger.error(f"Failed to run IPO alert: {e}")
        return 1


def handle_health_command(args) -> int:
    """Handle the health check command."""
    try:
        app = IPOAlert()
        checks = app.health_check()

        print("\n🏥 System Health Check")
        print("=" * 40)

        all_healthy = True
        for check_name, status in checks.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {check_name.replace('_', ' ').title()}: {'OK' if status else 'FAILED'}")
            if not status:
                all_healthy = False

        overall_status = "✅ HEALTHY" if all_healthy else "⚠️  ISSUES DETECTED"
        print(f"\nOverall Status: {overall_status}")

        return 0 if all_healthy else 1

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return 1


def handle_stats_command(args) -> int:
    """Handle the stats command."""
    try:
        app = IPOAlert()
        stats = app.get_stats()

        print("\n📊 Application Statistics")
        print("=" * 40)

        # Database stats
        db_stats = stats.get("database", {})
        print(f"📈 Total Notifications: {db_stats.get('total_notifications', 0)}")

        if db_stats.get('first_notification'):
            print(f"🗓️  First Notification: {db_stats['first_notification']}")
            print(f"🗓️  Last Notification: {db_stats['last_notification']}")

        print(f"💾 Database Size: {db_stats.get('database_size_kb', 0)} KB")

        # Config stats
        config_stats = stats.get("configuration", {})
        print(f"📧 Recipients: {config_stats.get('recipient_count', 0)}")
        print(f"🌐 Source URL: {config_stats.get('source_url', 'N/A')}")

        return 0

    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        return 1


def handle_cleanup_command(args) -> int:
    """Handle the cleanup command."""
    try:
        app = IPOAlert()
        success = app.cleanup(days_to_keep=args.days)

        if success:
            print(f"🧹 Cleanup completed successfully (kept records from last {args.days} days)")
            return 0
        else:
            print("❌ Cleanup failed")
            return 1

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate handler
    handlers = {
        "run": handle_run_command,
        "health": handle_health_command,
        "stats": handle_stats_command,
        "cleanup": handle_cleanup_command
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)