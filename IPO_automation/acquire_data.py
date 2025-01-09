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

    headings = extract_table_headings(ipo_div)
    data = extract_table_data(table_body)

    open_ipo = get_open_ipo_row(data, headings)

    return {
        "headings": list(headings.keys()),
        "data": data,
        "open_ipo": open_ipo,
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


def get_open_ipo_row(data, heading_map):
    """
    Finds the first row where the 'Status' column has the value 'open'.
    """
    # Get the index of the 'Status' column
    status_col = heading_map.get("Status")
    if status_col is None:
        raise IPOExtractionError("Status column not found.")

    # Loop through rows and check the 'Status' column
    for row in data:
        if row[status_col].strip().lower() == "open":
            return row

    return None  # No open IPO found


def extract_table_headings(ipo_div):
    """
    Maps table headings (from <th> tags) to their column indices.
    """
    # Extract and clean headings
    # headings = []
    # for th in safe_search(ipo_div, "find_all", "th") or []: # safe_search(ipo_div, "find_all", th) ->ipo_div.find_all("th")
    #     cleaned_text = clean_text(th.text)
    #     headings.append(cleaned_text)
    headings = [
        clean_text(th.text) for th in safe_search(ipo_div, "find_all", "th") or []
    ]
    if not headings:
        raise IPOExtractionError("No table headings found.")

    # Create a dictionary mapping headings to indices
    # a = {}
    # for index, heading in enumerate(headings):
    #     a[heading] = index
    # return a
    return {heading: index for index, heading in enumerate(headings)}


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

    try:
        result = ipo_details(html_data)
        print("\nTable Headings:")
        print(result["headings"])
        print("\nTable Data:")
        for row in result["data"]:
            print(row)
        if result["open_ipo"]:
            print("\nOpen IPO Details:")
            print(result["open_ipo"])
    except IPOExtractionError as e:
        print(f"Unexpected error: {e}")


# html_data = read_fetched(HTML_PATH)
# ipo_details(html_data)


if __name__ == "__main__":
    HTML_PATH = "data/share.html"
    try:
        test_ipo_extraction(HTML_PATH)
    except IPOExtractionError as e:
        print(f"Unexpected error: {e}")
