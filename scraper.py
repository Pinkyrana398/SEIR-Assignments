import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# hide all chrome stderr messages
sys.stderr = open(os.devnull, 'w')


# First we are checking if user has provided URL
if len(sys.argv) < 2:
    sys.exit()

# store URL in a variable url
url = sys.argv[1]

if not url.startswith("http"):
    url = "https://" + url


# setup headless chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# hide selenium logs
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)


service = Service(ChromeDriverManager().install(), log_path=os.devnull)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

# wait for javascript to load
time.sleep(5)

# scroll page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

page_content = driver.page_source
driver.quit()

# Change the html content in readable form
content = BeautifulSoup(page_content, "html.parser")


# Extract only title of the page
if content.title:
    title_text = content.title.get_text()
    print(title_text.strip())
else:
    print("\nTITLE:")
    print("No title found")


# Extract only body text of the page
if content.body:
    body_text = content.body.get_text(separator="\n", strip=True)
    print(body_text)
else:
    print("\nBODY:")
    print("No body content found") 


# Extract all links of the page 
allLinks = content.find_all("a")

found_link = False
for link in allLinks:
    hrefLink = link.get("href")
    if hrefLink:
        print(hrefLink)
        found_link = True
if not found_link:
    print("No links found")
