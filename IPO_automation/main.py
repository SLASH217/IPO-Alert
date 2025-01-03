# importing requests module to get content from online website
import requests


def fetchAndSave(url, path):
    # sending get request to the website
    response = requests.get(url, timeout=20)
    with open(path, "w", encoding="utf-8") as file:
        file.write(response.text)


# definining website url
site_url = "https://www.sharesansar.com"

fetchAndSave(site_url, "/data/share.html")
print("Data saved successfully")
