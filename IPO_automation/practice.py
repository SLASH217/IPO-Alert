import re
import requests
from bs4 import BeautifulSoup


try:
    response = requests.get("https://api.github.com/events")
    print(response.status_code)
    response.raise_for_status()  # Check for HTTP request errors
    print("Request was successful!")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")  # Print the error message
except Exception as e:
    print(f"An error occurred: {e}")  # Handle other potential errors


with open("test.html", "w", encoding="utf-8") as file:
    file.write(response.text)

with open("test.html", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
    print(type(content))


# try:
#     r = requests.get("https://api.github.com/events")
#     print(r.raise_for_status())
#     with open("test.html", "w", encoding="utf-8") as f:
#         f.write(r.text)
# except Exception as e:
#     print("Error: Get request failure.")
# # create html_doc string which is all the content of the html file in string form
# with open("test.html", "r", encoding="utf-8") as f:
#     html_doc = f.read()
#     print(html_doc)
# create a soup object
# soup = BeautifulSoup(html_doc, "html.parser")

# print(soup.prettify())
# print(soup.title.string)
# .string ra .text is the same thing
# print(soup.div.main.text)

# print(soup.find_all("div")[1]) #find_all le sabai elements find garcha ani returns a list.


# print(soup.find(id="god").text)
# find le thyo id lai search garcha if not found returns none. usually used to find links.

# get_text and just text seems to do the same thing
# for div in soup.find_all("span"):
#     print(div.get_text())
# nested div cha bhane this is print the div contents twice it seems.


# print(
#     soup.select("div.apple")
# )  # gives everything of the div as a list item. gives all divs with class apple.
# print(
#     soup.select("p#hey")
# )  # gives everything of the p as a list item. gives all p with id hey.
# print(soup.select_one("div.apple"))
# # gives the first div of the div as a item not enclosed in list brackets.
# print(soup.div.get("class")) # tells the name of the class of the first div ['apple', 'pehla'] list of classes


# print(soup.find(class_="dog"))  # since class itself is a keyword in python
# we have to use class_ instead of class. returns the first div with class dog. returns None if not found.
# find gives the first one, first_all gives all of them.


# print(soup.tbody.)

# for child in soup.select("div#eipo"):
#     print(child.text)


# def ipo_details(html):
#     soup = BeautifulSoup(html, "html.parser")
#     ipo_div = soup.find(id="eipo")
#     if ipo_div:
#         table_body = ipo_div.find(
#             "tbody"
#         )  # Narrow the scope to the specific tbody within the eipo div
#         if table_body:
#             data = []
#             rows = table_body.find_all("tr")  # Find all rows in the tbody
#             for row in rows:
#                 cols = []
#                 for col in row.find_all("td"):
#                     cleaned_text = clean_text(col)
#                     cols.append(cleaned_text)
#                 data.append(cols)

#             # Display the cleaned data
#             print("Table Data:")
#             print(data)

#         # Extract table headings within the same div
#         table_heading = [th.text.strip() for th in ipo_div.find_all("th")]
#         print(table_heading)
#         print("\nTable Headings:")


# def clean_text(element):
#     """
#     Cleans text by removing newlines, excess spaces, and stripping whitespace.

#     Args:
#         element (Tag): A BeautifulSoup element containing text.

#     Returns:
#         str: Cleaned text.
#     """
#     # Replace newlines and tabs with spaces
#     text = element.text.replace("\n", " ").replace("\t", " ")
#     # Use regex to replace multiple spaces with a single space
#     text = re.sub(r"\s+", " ", text)
#     # Strip leading and trailing spaces
#     return text.strip()


# ipo_details(html_doc)
