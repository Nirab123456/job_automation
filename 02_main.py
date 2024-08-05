# ==============================================================
#  00_main.py 
#  This program will scrape the Job Bank for job postings in a specified city
#  and stores them into an [html] file to be processed afterwards.
# ==============================================================

# ==============================================
#  CONSTANTS - MODULES
# ==============================================
from modules.ScrappySettings import Scrappy
from modules.CADGeo import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
from bs4 import BeautifulSoup
from datetime import date
import math

# ==============================================
#  FUNCTION
# ==============================================
def saveHTMLtoFile(fileName: str, html_content: str) -> None:
    outputFolder: str = "./test/" if Scrappy["debugMode"] else "./unparsedHTML/"
    with open(outputFolder + fileName, 'w', encoding='utf-8') as myFile:
        myFile.write(html_content)
    print(f"End of Copying HTML to {outputFolder + fileName}....\n")

# ==============================================
#  VARIABLES
# ==============================================
province_of_interest = 'ON'
city = "Toronto"

# Program Starts
print("\n\n")
print("Program Started...")

cityQ: str = city.replace(" ", "+")
provQ: str = province_of_interest.replace(" ", "+")

searchLink: str = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=&locationstring={cityQ}%2C+{provQ}&d=15"

# Retrieving Post Counts
content = requests.get(searchLink).text
soup = BeautifulSoup(content, 'lxml')
postTag = soup.find('span', class_="found", role="status")

if postTag is None:
    print(f"No job postings found for {city}")
else:
    postCnt = int(postTag.text.replace(",", ""))
    time.sleep(5)

    clickMore: int = math.ceil((postCnt - 25) / 25)

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(searchLink)
    wait = WebDriverWait(driver, 10)

    # Debugging Notes
    print("\n")
    print(f"{city} | Post: {postCnt} | Click: {clickMore}")

    # Expand all postings
    while True:
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.ID, 'moreresultbutton')))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)  # Scroll to button if necessary
            load_more_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error or no more results to load: {e}")
            print(f"{city} city is done Processing...")
            break

    # Save HTML content
    html_content = driver.page_source
    outputFile: str = province_of_interest + "-" + city.replace(" ", "-") + "-jobPostings.html"
    saveHTMLtoFile(outputFile, html_content)
    time.sleep(3)

    # Close Browser
    driver.quit()

    # Debugging Notes
    print(outputFile)
    print(searchLink)

    print("\n======================")
    print(" Program End")
    print("======================\n")

    raise SystemExit
