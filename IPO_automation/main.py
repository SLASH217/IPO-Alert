import requests
import re
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# Load environment variables
load_dotenv()


class IPOExtractionError(Exception):
    """Custom exception for IPO extraction errors."""


def fetch_and_save(url, path):
    """Fetch website content and save it locally."""
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print("Data saved successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def read_fetched(file_name):
    """Read data from a file and return as a string."""
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def ipo_details(html):
    """Extract IPO details from the given HTML content."""
    DIV_ID = "eipo"
    T_BODY = "tbody"

    soup = BeautifulSoup(html, "html.parser")
    ipo_div = safe_search(soup, "find", id=DIV_ID)
    if not ipo_div:
        raise IPOExtractionError("IPO section not found.")

    table_body = safe_search(ipo_div, "find", T_BODY)
    if not table_body:
        raise IPOExtractionError("IPO body not found.")

    headings = extract_table_headings(ipo_div)
    data = extract_table_data(table_body)
    open_ipo = get_open_ipo_row(data, headings)

    return {"headings": list(headings.keys()), "data": data, "open_ipo": open_ipo}


def extract_table_data(table_body):
    """Extract table data from a BeautifulSoup table body."""
    data = []
    rows = safe_search(table_body, "find_all", "tr")
    if not rows:
        return data
    for row in rows:
        cols = [
            clean_text(col.text) for col in safe_search(row, "find_all", "td") or []
        ]
        data.append(cols)
    return data


def get_open_ipo_row(data, heading_map):
    """Find the first row where the 'Status' column has the value 'open'."""
    status_col = heading_map.get("Status")
    if status_col is None:
        raise IPOExtractionError("Status column not found.")
    for row in data:
        if row[status_col].strip().lower() == "open":
            return row
    return None


def extract_table_headings(ipo_div):
    """Map table headings (from <th> tags) to their column indices."""
    headings = [
        clean_text(th.text) for th in safe_search(ipo_div, "find_all", "th") or []
    ]
    if not headings:
        raise IPOExtractionError("No table headings found.")
    return {heading: index for index, heading in enumerate(headings)}


def safe_search(obj, method, *args, **kwargs):
    """Safely search for a method on an object, return None if AttributeError occurs."""
    try:
        return getattr(obj, method)(*args, **kwargs)
    except AttributeError:
        return None


def clean_text(element):
    """Clean text by removing newlines, excess spaces, and stripping whitespace."""
    text = element.replace("\n", " ").replace("\t", " ")
    return re.sub(r"\s+", " ", text).strip()


def send_email(subject, body, to_email):
    """Send an email using SMTP."""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def prepare_ipo_email(open_ipo):
    """Prepare an email for open IPO notifications."""
    if not open_ipo:
        return None, None
    subject = f"IPO Open: {open_ipo[2]}"
    body = f"""
    Hello,

    The following IPO is now open for application:

    Company Name: {open_ipo[2]}
    Units Available: {open_ipo[3]}
    Price per Unit: {open_ipo[4]}
    Start Date: {open_ipo[5]}
    End Date: {open_ipo[6]}

    Visit the official site to apply now!
    https://meroshare.cdsc.com.np

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
        notified_ipos = load_notified_ipos()
        result = ipo_details(html_data)
        open_ipo = result.get("open_ipo")
        if not open_ipo:
            print("No open IPOs to notify.")
            return

        ipo_identifier = open_ipo[2]
        if ipo_identifier in notified_ipos:
            print(f"Already notified about IPO: {ipo_identifier}")
            return

        subject, body = prepare_ipo_email(open_ipo)
        if subject and body:
            send_email(subject, body, recipient_email)
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
        return set()


def save_notified_ipo(identifier, log_file="notified_ipos.txt"):
    """Save a notified IPO identifier to the log file."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{identifier}\n")


if __name__ == "__main__":
    HTML_URL = "https://www.sharesansar.com"
    HTML_PATH = "C:/Users/Admin/Videos/Desktop/IPO-Alert/IPO_automation/data/share.html"

    RECIPIENT_EMAIL = "prashannadahal217@gmail.com"

    fetch_and_save(HTML_URL, HTML_PATH)
    notify_ipo(HTML_PATH, RECIPIENT_EMAIL)
