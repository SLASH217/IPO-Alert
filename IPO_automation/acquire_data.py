import re
from bs4 import BeautifulSoup
from fetch_save_00 import read_fetched


class IPOExtractionError(Exception):
    """Custom exception for IPO extraction errors."""


def ipo_details(html):
    """Extract IPO details from the given HTML content."""
    DIV_ID = "eipo"
    T_BODY = "tbody"
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Target IPO section of the webpage
    ipo_div = safe_search(soup, "find", id=DIV_ID)  # equivalent to soup.find(id="eipo")
    if not ipo_div:
        raise IPOExtractionError("IPO section not found.")

    # Narrow the scope to the specific tbody within the IPO div
    table_body = safe_search(
        ipo_div, "find", T_BODY
    )  # equivalent to soup.find("tbody")
    if not table_body:
        raise IPOExtractionError("IPO body not found.")

    # Extract table headings and data
    headings = extract_table_headings(ipo_div)
    data = extract_table_data(table_body)

    # Find any open IPOs
    open_ipo = get_open_ipo_row(data)

    return {
        "headings": headings or [],
        "data": data or [],
        "open_ipo": open_ipo or None,
    }


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


def get_open_ipo_row(data):
    """Check if at least one IPO is open and return a boolean."""
    for tr in data:
        if tr[-2].lower() == "open":
            # print(tr)
            return tr
    return False


def extract_table_headings(ipo_div):
    """Extract and clean table headings from a given div."""
    return [
        clean_text(th.text) for th in (safe_search(ipo_div, "find_all", "th") or [])
    ]


def safe_search(obj, method, *args, **kwargs):
    """Safely search for a method on an object, return None if AttributeError occurs."""
    try:
        return getattr(obj, method)(*args, **kwargs)
    except AttributeError:
        return None


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


def test_ipo_extraction(html_path):
    """Test function to extract IPO details and print them."""
    html_data = read_fetched(html_path)
    if not html_data:
        print("Failed to read HTML data.")
        return

    result = ipo_details(html_data)

    # Handle errors
    if "error" in result:
        print(result["error"])
        return

    # Display results in the terminal for debugging
    print("\nTable Headings:")
    print(result["headings"])
    print("\nTable Data:")
    for row in result["data"]:
        print(row)
    if result["open_ipo"]:
        print("\nOpen IPO Details:")
        print(result["open_ipo"])


# html_data = read_fetched(HTML_PATH)
# ipo_details(html_data)


if __name__ == "__main__":
    HTML_PATH = "data/share.html"
    try:
        test_ipo_extraction(HTML_PATH)
    except IPOExtractionError as e:
        print(f"Unexpected error: {e}")
