# IPO Alert Automation Project

Welcome to the **IPO Alert Automation Project**! This project is designed to fetch the latest IPO details from [Sharesansar](https://www.sharesansar.com), process the data, and send notifications to specified email addresses. It's an efficient and automated solution to keep track of IPOs effortlessly.

## 🌟 Features

- **Automated Web Scraping**: Fetches IPO data directly from Sharesansar
- **Smart Email Notifications**: Sends detailed IPO alerts to multiple recipients
- **Duplicate Prevention**: Tracks already-notified IPOs to avoid redundancy
- **Robust Error Handling**: Comprehensive error handling and logging
- **Health Monitoring**: Built-in health checks and system monitoring
- **Command Line Interface**: Easy-to-use CLI with multiple commands
- **Modular Design**: Clean, maintainable, and extensible codebase
- **Comprehensive Testing**: Unit tests for critical components
- **Retry Logic**: Automatic retry for network operations

## 🚨 Disclaimer
This project is specifically designed for IPOs in Nepal, targeted towards Nepali citizens. It only supports IPO notifications and does not include information about FPOs (Follow-on Public Offers) or Right Shares.

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Gmail account with 2-factor authentication enabled**
- **Gmail App Password** (not your regular password)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/SLASH217/IPO-Alert.git
cd IPO-Alert
python setup.py
```

The setup script will:
- Check Python version compatibility
- Install all dependencies
- Create necessary directories
- Help you configure environment variables
- Run health checks

### 2. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 3. Configure Environment

Edit `.env` file with your details:

```bash
EMAIL_ADDRESS=your_email@gmail.com
APP_PASSWORD=your_app_password
RECIPIENT_EMAIL_LIST=recipient1@email.com,recipient2@email.com
```

**Important**: For Gmail, you need an **App Password**, not your regular password:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password at: https://myaccount.google.com/apppasswords
3. Use this App Password in the configuration

## 📁 Project Structure

```
IPO-Alert/
├── src/                     # Source code
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── database.py         # Data storage and management
│   ├── email_service.py    # Email functionality
│   ├── logger.py           # Logging configuration
│   ├── main_app.py         # Main application logic
│   ├── models.py           # Data models
│   └── scraper.py          # Web scraping logic
├── tests/                  # Unit tests
│   ├── test_config.py
│   ├── test_models.py
│   └── ...
├── data/                   # Data storage
├── logs/                   # Application logs
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml
│       └── cloud-automation.yml
├── scripts/                # Automation scripts
│   ├── health_check.sh
│   └── setup_env.sh
├── main.py                 # Main entry point
├── cli.py                  # Command line interface
├── setup.py                # Setup script
├── .env.example            # Environment template
└── requirements.txt        # Dependencies
```

## 🖥️ Usage

### Basic Usage

```bash
# Run IPO alert process
python main.py

# Or using CLI
python cli.py run
```

### CLI Commands

```bash
# Run with options
python cli.py run --dry-run      # Test without sending emails
python cli.py run --force        # Force send even if already notified

# System monitoring
python cli.py health             # Check system health
python cli.py stats              # Show statistics

# Maintenance
python cli.py cleanup            # Clean old records (30 days)
python cli.py cleanup --days 60  # Clean records older than 60 days

# Help
python cli.py --help             # Show all commands
```

## � **Automation Setup** (Choose One)

### **Option 1: Cloud Automation (Recommended) ⭐**

Perfect for 24/7 operation even when your laptop is off!

📖 **[Complete GitHub Actions Setup Guide](GITHUB_ACTIONS_SETUP.md)**

**Quick setup:**
1. Push code to GitHub
2. Add 3 secrets in GitHub repo settings
3. Enable GitHub Actions
4. Runs automatically at 9 AM & 4 PM IST daily

### **Option 2: Local Automation**

For running on your local machine only when it's on:

1. **Make scripts executable**:
   ```bash
   chmod +x setup_automation.sh
   chmod +x scripts/health_check.sh
   ```

2. **Run the automation setup**:
   ```bash
   ./setup_automation.sh
   ```

3. **Verify automation**:
   ```bash
   # Check if timer is active
   sudo systemctl status ipo-alert.timer

   # Check upcoming runs
   sudo systemctl list-timers ipo-alert.timer
   ```

### **Manual Testing**

```bash
# Test the health check
./scripts/health_check.sh

# Run a manual check
python main.py

# Check system stats
python -c "from src.database import DatabaseManager; db = DatabaseManager(); print(db.get_stats())"
```

## �🔧 Configuration Options

| Environment Variable | Required | Description | Default |
|---------------------|----------|-------------|---------|
| `EMAIL_ADDRESS` | Yes | Your Gmail address | - |
| `APP_PASSWORD` | Yes | Gmail App Password | - |
| `RECIPIENT_EMAIL_LIST` | Yes | Comma-separated recipient emails | - |
| `SOURCE_URL` | No | IPO data source URL | `https://www.sharesansar.com` |
| `DATA_PATH` | No | Path to save HTML data | `data/share.html` |
| `NOTIFIED_IPOS_FILE` | No | Path to notification database | `data/ipo_history.json` |
| `LOG_LEVEL` | No | Logging level | `INFO` |

## 📊 Monitoring and Logging

### Health Checks

The system includes comprehensive health checks:

```bash
python cli.py health
```

Checks include:
- ✅ Configuration validation
- ✅ Email connection test
- ✅ Source website accessibility
- ✅ Database accessibility

### Logging

Logs are stored in `logs/ipo_alert.log` with rotation:
- Maximum file size: 1MB
- Backup files: 5
- Format: Timestamp, level, function, line number, message

### Statistics

View application statistics:

```bash
python cli.py stats
```

Shows:
- Total notifications sent
- First/last notification dates
- Database size
- Configuration summary

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🔒 Security Features

- **Environment Variables**: Sensitive data stored securely
- **App Passwords**: Uses Gmail App Passwords instead of account passwords
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: No sensitive information in error messages

## 🚨 Troubleshooting

### Common Issues

1. **Email Authentication Failed**
   - Ensure 2-factor authentication is enabled
   - Use App Password, not account password
   - Check email address is correct

2. **No IPOs Found**
   - Check internet connection
   - Verify source website is accessible
   - Check logs for detailed error information

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **Permission Errors**
   - Ensure write permissions for `data/` and `logs/` directories
   - Run with appropriate user permissions

### Getting Help

1. Check logs in `logs/ipo_alert.log`
2. Run health check: `python cli.py health`
3. Test configuration: `python cli.py run --dry-run`
4. Open an issue on GitHub with log details

## 🔮 Future Enhancements

- [ ] **Web Dashboard**: Web interface for monitoring and configuration
- [ ] **SMS Notifications**: Add SMS alert support
- [ ] **Multiple Sources**: Support for additional IPO data sources
- [ ] **Scheduling**: Built-in scheduler for automated runs
- [ ] **Docker Support**: Containerized deployment
- [ ] **API Integration**: REST API for external integrations
- [ ] **Mobile App**: Mobile application for notifications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/SLASH217/IPO-Alert.git
cd IPO-Alert
python setup.py
pip install pytest black flake8
```

### Code Style

- Use Black for code formatting: `black src/`
- Follow PEP 8 guidelines
- Add type hints where appropriate
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: Prashanna Dahal
- **Email**: prashanna217@gmail.com
- **GitHub**: [SLASH217](https://github.com/SLASH217)

## 🙏 Acknowledgments

- [Sharesansar](https://www.sharesansar.com) for providing IPO data
- Python community for excellent libraries
- Contributors and users for feedback and suggestions

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**
Price per Unit: NPR 100
Start Date: 2025-01-15
End Date: 2025-01-25

Visit the official site to apply now:
https://meroshare.cdsc.com.np

Best regards,
IPO Tracker Team
```

---

## Future Enhancements

- Add support for additional data sources.
- Integrate a dashboard to view and manage IPO alerts.
- Add SMS notification support.
- Enhance error logging and monitoring.

---

## License
This project is licensed under the MIT License.

---

## Contributions
Contributions, issues, and feature requests are welcome! Feel free to fork this repository and submit a pull request.

---

## Contact
For any queries, reach out to:
- **Author**: Prashanna Dahal
- **Email**: prashanna217@gmail.com
- **GitHub**: [SLASH217](https://github.com/SLASH217)
