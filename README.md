import json
from bs4 import BeautifulSoup

# Load the HTML file
with open("yourfile.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extract data (example: extract key-value pairs)
data = {}
for item in soup.find_all("div", class_="item"):  # Adjust selector as needed
    key = item.find("span", class_="key").text.strip()
    value = item.find("span", class_="value").text.strip()
    data[key] = value

# Save to JSON
with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4)
