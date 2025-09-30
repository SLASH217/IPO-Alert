#!/bin/bash

# IPO Alert Automation Setup Script for Arch Linux
# This script sets up systemd timer to run IPO alerts twice daily

set -e

echo "🤖 Setting up IPO Alert Automation..."
echo "This will run IPO checks at 9:00 AM and 4:00 PM daily"
echo

# Check if running as regular user
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root. Run as your regular user."
    exit 1
fi

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if project is set up
if [ ! -f "$SCRIPT_DIR/ipo-alert.sh" ]; then
    echo "❌ IPO Alert script not found. Please run setup first."
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "❌ .env file not found. Please configure your email settings first."
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Test the application
echo "🧪 Testing IPO Alert application..."
if ! "$SCRIPT_DIR/ipo-alert.sh" health > /dev/null 2>&1; then
    echo "❌ IPO Alert health check failed. Please fix configuration first."
    echo "   Run: ./ipo-alert.sh health"
    exit 1
fi

echo "✅ IPO Alert application is working correctly"
echo

# Install systemd service files
echo "📝 Installing systemd service files..."

# Copy service file
sudo cp "$SCRIPT_DIR/systemd/ipo-alert.service" /etc/systemd/system/
echo "✅ Installed ipo-alert.service"

# Copy timer file
sudo cp "$SCRIPT_DIR/systemd/ipo-alert.timer" /etc/systemd/system/
echo "✅ Installed ipo-alert.timer"

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable the timer
echo "⚡ Enabling IPO Alert timer..."
sudo systemctl enable ipo-alert.timer

# Start the timer
echo "🚀 Starting IPO Alert timer..."
sudo systemctl start ipo-alert.timer

# Show status
echo
echo "📊 Timer Status:"
sudo systemctl status ipo-alert.timer --no-pager -l

echo
echo "📅 Scheduled runs:"
systemctl list-timers ipo-alert* --no-pager

echo
echo "🎉 IPO Alert Automation Setup Complete!"
echo
echo "📋 What happens now:"
echo "   • IPO alerts will run automatically at 9:00 AM and 4:00 PM daily"
echo "   • Logs will be available via: sudo journalctl -u ipo-alert.service"
echo "   • You can check status with: sudo systemctl status ipo-alert.timer"
echo
echo "🔧 Useful commands:"
echo "   • Test manually: ./ipo-alert.sh run --dry-run"
echo "   • Check logs: sudo journalctl -u ipo-alert.service -f"
echo "   • Stop automation: sudo systemctl stop ipo-alert.timer"
echo "   • Start automation: sudo systemctl start ipo-alert.timer"
echo "   • Disable automation: sudo systemctl disable ipo-alert.timer"
echo
echo "✅ Setup completed successfully!"