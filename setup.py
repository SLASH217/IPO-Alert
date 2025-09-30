#!/usr/bin/env python3
"""
Setup script for IPO Alert application.
This script helps users set up the environment and dependencies.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"🔄 {description}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False

    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def install_dependencies():
    """Install required dependencies."""
    requirements_file = "requirements.txt"

    if not Path(requirements_file).exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        return False

    return run_command(
        f"pip install -r {requirements_file}",
        "Installing dependencies"
    )


def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

    return True


def setup_environment_file():
    """Help user set up environment file."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("✅ .env file already exists")
        return True

    if not env_example.exists():
        print("❌ .env.example file not found")
        return False

    print("\n🔧 Setting up environment configuration...")
    print("You need to create a .env file with your email configuration.")
    print(f"Template available at: {env_example}")

    response = input("\nWould you like to create .env file now? (y/N): ").lower().strip()

    if response in ['y', 'yes']:
        try:
            # Copy example file
            with open(env_example, 'r') as src:
                content = src.read()

            print("\nPlease provide the following information:")

            # Get user input
            email = input("Your Gmail address: ").strip()
            while not email or '@' not in email:
                email = input("Please enter a valid email address: ").strip()

            app_password = input("Your Gmail App Password: ").strip()
            while not app_password:
                app_password = input("App password cannot be empty: ").strip()

            recipients = input("Recipient emails (comma-separated): ").strip()
            while not recipients:
                recipients = input("Please enter at least one recipient: ").strip()

            # Replace placeholders
            content = content.replace("your_email@gmail.com", email)
            content = content.replace("your_app_password", app_password)
            content = content.replace("recipient1@email.com,recipient2@email.com", recipients)

            # Write .env file
            with open(env_file, 'w') as dst:
                dst.write(content)

            print("✅ .env file created successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print(f"⚠️  Please manually copy {env_example} to .env and fill in your details")
        return False


def test_setup():
    """Test if the setup is working."""
    print("\n🧪 Testing setup...")

    try:
        # Try importing our modules
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from src.config import Config
        from src.main_app import IPOAlert

        # Test configuration loading
        config = Config.from_env()
        config.validate()

        print("✅ Configuration loaded successfully")

        # Test app initialization
        app = IPOAlert()
        health = app.health_check()

        print("\n🏥 Health Check Results:")
        for check, status in health.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {check.replace('_', ' ').title()}")

        all_good = all(health.values())
        if all_good:
            print("\n🎉 Setup completed successfully! You can now run the application.")
        else:
            print("\n⚠️  Some health checks failed. Please review the configuration.")

        return all_good

    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 IPO Alert Setup")
    print("=" * 50)

    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment_file),
        ("Testing setup", test_setup)
    ]

    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")

        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please resolve the issues and run setup again.")
            sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Review your .env file configuration")
    print("2. Run: python main.py")
    print("3. Or run: python cli.py run --dry-run (to test without sending emails)")
    print("\nFor more options, run: python cli.py --help")


if __name__ == "__main__":
    main()