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

import pyautogui
import time
import webbrowser
import math
import win32clipboard
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

# ==============================================
#  FUNCTION
# ==============================================
def saveHTMLtoFile(fileName: str) -> None:
    waitTime: float = 1
    outputFolder: str = "./test/" if Scrappy["debugMode"] else "./unparsedHTML/"

    pyautogui.moveTo(178, 369, 0.25)
    time.sleep(waitTime)
    pyautogui.click()
    time.sleep(waitTime)
    pyautogui.press('f12')
    time.sleep(waitTime + 10)

    pyautogui.moveTo(1167, 175, 0.25)
    time.sleep(waitTime)
    pyautogui.click()
    time.sleep(waitTime)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(waitTime)

    win32clipboard.OpenClipboard()
    with open(outputFolder + fileName, 'w', encoding='utf-8') as myFile:
        myFile.write(win32clipboard.GetClipboardData())
    win32clipboard.CloseClipboard()

    pyautogui.press('f12')
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

    # Open Browser and Expand all Jobs
    webbrowser.open(searchLink)
    time.sleep(20)

    # Debugging Notes
    print("\n")
    print(f"{city} | Post: {postCnt} | Click: {clickMore}")

    # Expand all postings
    while True:
        pyautogui.moveTo(1100, 600, 0.25)
        pyautogui.click()

        time.sleep(5)
        pyautogui.keyDown('end')
        pyautogui.keyUp('end')

        if clickMore == 0:
            print(f"{city} city is done Processing...")
            break

        clickMore -= 1
        print(f"Paginate: {clickMore}")

        if clickMore % 20 == 0:
            time.sleep(10)  # Take a break

    outputFile: str = province_of_interest + "-" + city.replace(" ", "-") + "-jobPostings.html"
    saveHTMLtoFile(outputFile)
    time.sleep(3)

    # Close Browser
    pyautogui.moveTo(380, 20, 0.25)
    pyautogui.click(button='middle')

    # Debugging Notes
    print(outputFile)
    print(searchLink)

    print("\n======================")
    print(" Program End")
    print("======================\n")

    raise SystemExit
