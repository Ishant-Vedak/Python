from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json
import pandas as pd
from notion_client import Client
from dotenv import load_dotenv
import os

'''  .\.venv\Scripts\activate  '''

allScholarships = []

load_dotenv()

duration = 80
options = Options()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(service=Service(), options=options)

website = "https://google.com"
driver.get(website)

def Waitfor(time_waiting: int, selector: str, identifier: str): 
    WebDriverWait(driver, time_waiting).until(
        EC.presence_of_element_located((selector, identifier))
    )

def find(selector: str, identifier: str):
    el = driver.find_element(selector, identifier)
    return el

def findAndSendKeys(selector: By, identifier: str, keys: str, *keyboard_input: str):
    var_name = find(selector, identifier)
    if keyboard_input:
        var_name.send_keys(keys, *keyboard_input)
    else:
        var_name.send_keys(keys)
    return var_name

def findAndClick(selector: By, identifier: str):
    var_name = find(selector, identifier)
    var_name.click()
    return var_name


Waitfor(5, By.CLASS_NAME, "gLFyf")
findAndSendKeys(By.CLASS_NAME, "gLFyf", "scholartree.com", Keys.ENTER)
Waitfor(30, By.XPATH, "//h3")
findAndClick(By.PARTIAL_LINK_TEXT, "ScholarTree")
Waitfor(20, By.XPATH, "//a")
findAndClick(By.XPATH, "//a[contains(@href,'/login')]")
Waitfor(20, By.XPATH, "//input")
findAndSendKeys(By.XPATH, "//input[@placeholder='E-mail']", os.getenv("SCHOLAR_USERNAME"))
findAndSendKeys(By.XPATH, "//input[@placeholder='Password']", os.getenv("SCHOLAR_PASSWORD"))
findAndClick(By.XPATH, "//button[text()='Log in']")
driver.implicitly_wait(5)
findAndClick(By.XPATH, "//div[contains(text(), 'Favourite')]")
while True:
    try:
        findAndClick(By.XPATH, "//button[contains(text(), 'Load more')]")
        time.sleep(2)
    except NoSuchElementException:
        break

items = driver.find_elements(By.CLASS_NAME, "scholarship-list-item")
itemsListCount = len(items)

for i in range(itemsListCount):
    items = driver.find_elements(By.CLASS_NAME, "scholarship-list-item")
    heading = items[i].text
    items[i].click()
    Waitfor(3, By.XPATH, "//h1")
    allScholarships.append(heading)
    driver.back()
    Waitfor(5, By.CLASS_NAME, "scholarship-list-item")
duration -= duration
time.sleep(duration)
driver.quit()

split_scholarships = [scholarship.split('\n') for scholarship in allScholarships]

scholarship_dict = [{"id": idx, "Name": i[0], "Amount": i[1], "Date": i[2], "Requirements": i[3:]} for idx, i in enumerate(split_scholarships)]

print(f"There are {len(scholarship_dict)} scholarships favorited")
df = pd.DataFrame(scholarship_dict)


df.to_json("scholarships.json", orient="records", indent=2, force_ascii=False)

'''   need to add each scholarship to a db.   '''

notion = Client(auth=os.getenv("WORKING_NOTION_API_KEY"))

for _, scholarship in df.iterrows():
    open_or_closed = ""
    if str(scholarship["Date"]).startswith("D"):
        open_or_closed = "Open"
    else: 
        open_or_closed = "Closed"
    
    req_str = ""
    for requirement in scholarship["Requirements"]:
        req_str += str(requirement) + " "
        
    notion.pages.create(
        parent={"database_id": os.getenv("WORKING_DB_KEY")},
        properties={
            "Name": {
                "title": [{"text": {"content": scholarship["Name"]}}]
                },
            "Amount": {
                "rich_text": [{"text": {"content": str(scholarship["Amount"])}}]
                },
            "Date": {
                "rich_text": [{"text": {"content": str(scholarship["Date"])}}]
                },
            "Requirements": {
                "rich_text": [{"text": {"content": req_str}}]
                },
            "Open or Closed?": {
                "select": {"name": open_or_closed}
                },
            "Completed": {
                "select": {"name": "Not Completed"}
                },
        }
    )

'''   check the db if the scholarship already exists. '''

''' add scholarship titles to google calendar'''

'''  check calendar if the scholarship already exists. '''

'''   maybe be able to change properties'''