# IPO Alert Automation Project

Welcome to the **IPO Alert Automation Project**! This project is designed to fetch the latest IPO details from [Sharesansar](https://www.sharesansar.com), process the data, and send notifications to specified email addresses. It's an efficient and automated solution to keep track of IPOs effortlessly.

---

## Features

- **Automated Web Scraping**: Fetches IPO data directly from Sharesansar.
- **Custom Email Notifications**: Sends detailed IPO alerts to multiple recipients.
- **Error Handling**: Robust mechanisms to handle data extraction and email sending errors.
- **Duplicate Notification Prevention**: Keeps track of already-notified IPOs to avoid redundancy.
- **Modular Design**: Each function is independently reusable and maintainable.

---

## Disclaimer
This project is specifically designed for IPOs in Nepal, targeted towards Nepali citizens. It only supports IPO notifications and does not include information about FPOs (Follow-on Public Offers) or Right Shares.

---

## Installation

### Prerequisites
- Python 3.8 or above
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `smtplib`

Install the dependencies using pip:
```bash
pip install requests beautifulsoup4
```

---

## Project Structure

```
IPO-Alert/
├── data/
│   └── share.html               # Saved HTML data from Sharesansar
├── main.py                  # Main script
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## Usage

### 1. Set Up Environment Variables
Create a `.env` file or set the following environment variables:

```bash
EMAIL_ADDRESS="your_email@example.com"     # Sender's email address
APP_PASSWORD="your_app_password"          # Sender's email password
RECIPIENT_EMAIL="recipient1@example.com"  # First recipient email
DIJU_MAIL="recipient2@example.com"        # Second recipient email
```

### 2. Run the Script

```bash
python ipo_alert.py
```

The script will:
1. Fetch IPO details from Sharesansar.
2. Save the data locally.
3. Notify recipients via email.

---

## Key Functions

### 1. `fetch_and_save(url, path)`
Fetches the IPO page HTML data and saves it to the specified file path.

### 2. `notify_ipo(html_path, recipient_email)`
Processes the HTML data, extracts IPO details, and sends email notifications to the recipient.

### 3. `send_email(subject, body, to_email)`
Handles email sending using SMTP with Gmail servers.

---

## Example Notification

**Subject:** IPO Open: Company XYZ

**Body:**
```
Hello,

The following IPO is now open for application:

Company Name: XYZ
Units Available: 1,000,000
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
