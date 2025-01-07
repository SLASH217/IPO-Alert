import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
from email.message import EmailMessage
from acquire_data import read_fetched, IPOExtractionError, ipo_details


def send_email(subject, body, to_email):
    """Send an email using SMTP."""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    # Create an EmailMessage object
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    # Connect to the SMTP server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def prepare_ipo_email(open_ipo):
    """Prepare an email for open IPO notifications."""
    if not open_ipo:
        return None, None  # No open IPOs

    subject = f"IPO Open: {open_ipo[2]}"  # Example: "IPO Open: Guardian Micro Life Insurance Limited"
    body = f"""
    Hello,

    The following IPO is now open for application:

    Company Name: {open_ipo[2]}
    Units Available: {open_ipo[3]}
    Price per Unit: {open_ipo[4]}
    Start Date: {open_ipo[5]}
    End Date: {open_ipo[6]}

    Visit the official site to apply now!

    Best regards,
    IPO Tracker Team
    """
    return subject, body


def notify_ipo(html_path, recipient_email):
    """Extract IPO details and send an email notification for open IPOs."""
    html_data = read_fetched(html_path)
    if not html_data:
        print("Failed to read HTML data.")
        return

    try:
        # Load previously notified IPOs
        notified_ipos = load_notified_ipos()

        result = ipo_details(html_data)
        open_ipo = result.get("open_ipo")
        if not open_ipo:
            print("No open IPOs to notify.")
            return

        ipo_identifier = open_ipo[
            2
        ]  # Assuming the company name uniquely identifies an IPO

        # Check if the IPO has already been notified
        if ipo_identifier in notified_ipos:
            print(f"Already notified about IPO: {ipo_identifier}")
            return

        # Prepare and send the email
        subject, body = prepare_ipo_email(open_ipo)
        if subject and body:
            send_email(subject, body, recipient_email)
            # Log the notified IPO
            save_notified_ipo(ipo_identifier)
            print(f"Notification sent for IPO: {ipo_identifier}")
        else:
            print("No valid data to send email.")
    except IPOExtractionError as e:
        print(f"Error during IPO extraction: {e}")


def load_notified_ipos(log_file="notified_ipos.txt"):
    """Load the list of already notified IPOs from a file."""
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()  # If the file doesn't exist, return an empty set


def save_notified_ipo(identifier, log_file="notified_ipos.txt"):
    """Save a notified IPO identifier to the log file."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{identifier}\n")


if __name__ == "__main__":
    HTML_PATH = "data/share.html"
    RECIPIENT_EMAIL = "prashannadahal217@gmail.com"
    notify_ipo(HTML_PATH, RECIPIENT_EMAIL)
