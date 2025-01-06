import re
from bs4 import BeautifulSoup
from fetch_save_00 import read_fetched

HTML_PATH = "data/share.html"


def ipo_details(html):
    """Extract IPO details from the given HTML content."""
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Target IPO section of the webpage using safe_search
    ipo_div = safe_search(
        soup, "find", id="eipo"
    )  # equivalent to soup.find(id ="eipo")
    if not ipo_div:
        print("IPO section not found.")
        return

    # Narrow the scope to the specific tbody within the eipo div
    table_body = safe_search(
        ipo_div, "find", "tbody"
    )  # equivalent to soup.find("tbody")
    if not table_body:
        print("Table body not found.")
        return

    # Extract table data
    data = extract_table_data(table_body)
    headings = extract_table_headings(ipo_div)

    # Display the cleaned data in terminal and get the result ready for email function.
    if headings:
        print("\nTable Headings:")
        print(headings)
    if data:
        print("Table Data:")
        ipo_open = check_open(data)
        # if ipo_open:
        #     print("At least one IPO is open.")


def extract_table_data(table_body):
    """Extract table data from a BeautifulSoup table body."""
    data = []
    rows = safe_search(
        table_body, "find_all", "tr"
    )  # equivalent to soup.find_all("tr")
    if not rows:
        return data
    for row in rows:
        cols = []
        columns = safe_search(
            row, "find_all", "td"
        )  # equivalent to soup.find_all("td")
        if columns:
            for col in columns:
                cleaned_text = clean_text(col.text)
                cols.append(cleaned_text)
            data.append(cols)
    return data
    # data is a 2D array [['1', 'GMLIL', 'Guardian Micro Life Insurance Limited', '1,845,000.00', '100.00', '2025-01-05', '2025-01-08 Open', 'Open', ''], ['2', 'RSM', 'Reliance Spinning Mills', '1,155,960.00', '820.80', 'Coming Soon', 'Coming Soon Coming Soon', 'Coming Soon', '']]


def extract_table_headings(ipo_div):
    """Extract and clean table headings from a given div."""
    return [
        clean_text(th.text) for th in (safe_search(ipo_div, "find_all", "th") or [])
    ]


def clean_text(element):
    """
    Cleans text by removing newlines, excess spaces, and stripping whitespace.

    Args:
        element (Tag): A BeautifulSoup element containing text.

    Returns:
        str: Cleaned text.
    """
    # Replace newlines and tabs with spaces
    text = element.replace("\n", " ").replace("\t", " ")
    # Use regex to replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading and trailing spaces
    return text.strip()


def safe_search(obj, method, *args, **kwargs):
    """Safely search for a method on an object, return None if AttributeError occurs."""
    try:
        return getattr(obj, method)(*args, **kwargs)
    except AttributeError:
        return None


def check_open(data):
    """Check if at least one IPO is open and return a boolean."""
    for tr in data:
        if tr[-2].lower() == "open":
            print(tr)
            return True
    return False


html_data = read_fetched(HTML_PATH)

ipo_details(html_data)
