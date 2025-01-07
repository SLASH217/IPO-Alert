import requests


# Function to fetch website content and save it locally
def fetch_and_save(url, path):
    """performs a get request to sharesansar.com & saves data in html file."""
    try:
        # Send GET request to the website
        response = requests.get(url, timeout=20)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        with open(path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print("Data saved successfully!")
        # return response.text  # Return the HTML content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def read_fetched(file_name):
    """Converts the data from share.html into a large string making it appropriate to work with
    beautifulsoup.

    Args:
        file_name (path): Gives file_path to share.html

    Returns:
        str : The whole data of share.html as a string.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    HTML_PATH = "https://www.sharesansar.com"
    HTML_PATH = "data/share.html"
    fetch_and_save(HTML_PATH, HTML_PATH)
