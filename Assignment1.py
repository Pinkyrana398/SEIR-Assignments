import sys
# First we are checking if user has provided URL
if len(sys.argv) < 2:
    print("Please provide a URL")
    sys.exit()

# store URL in a variable url
url = sys.argv[1]
print("URL received:", url)


# Check if page fetched successfully or not
import requests
headers = {
    "User-Agent": "Mozilla/5.0"
}
try:
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()   
    page_content = response.text
    print("Page fetched successfully")
except requests.exceptions.RequestException as e:
    print("Error fetching the page:", e)
    sys.exit()


# Change the html content in readable form
from bs4 import BeautifulSoup

content = BeautifulSoup(page_content, "html.parser")
print("HTML parsed successfully")


# Extract only title of the page
if content.title:
    title_text = content.title.get_text()
    print("\nTITLE:")
    print(title_text.strip())
else:
    print("\nTITLE:")
    print("No title found")


# Extract only body text of the page
if content.body:
    body_text = content.body.get_text(separator="\n", strip=True)
    print("\nBODY:")
    print(body_text)
else:
    print("\nBODY:")
    print("No body content found") 


# Extract all links of the page 
print("\nLINKS:")
allLinks = content.find_all("a")

found_link = False
for link in allLinks:
    hrefLink = link.get("href")
    if hrefLink:
        print(hrefLink)
        found_link = True
if not found_link:
    print("No links found")
