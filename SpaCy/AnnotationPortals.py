from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchAttributeException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from CheckBiased import CheckBiased
import os, time, langdetect

load_dotenv()

link_groups = {
    "Israel2020_Jan-Apr": "1",
    "Israel2020_May-Aug": "2",
    "Israel2020_Sep-Dec": "3",
    "Israel2021_Jan-Apr": "4",
    "Israel2021_May-Aug": "5",
    "Israel2022_Jan-Apr": "9",
    "Israel2022_May-Aug": "10",
    "Israel2022_Sep-Dec": "11",
    "Israel2023_Dec_1-21": "12",
    "Israel2023_Jan-Apr": "13",
    "Israel2023_Nov_1-21": "14",
    "Jews2019.rep1": "15",
    "Jews2019.rep2": "16",
    "Jews2020_Jan-Apr.rep1": "17",
    "Jews2020_Jan-Apr.rep2": "18",
    "Jews2020_Sep-Dec.rep1": "19",
    "Jews2020_Sep-Dec.rep2": "20",
    "Jews2021_Jan-Apr": "21",
    "Jews2021_May-Aug": "22",
    "Jews2021_Sep-Dec": "23",
    "Jews2022_Jan-Apr": "24",
    "Jews2022_May-Aug": "25",
    "Jews2022_Sep-Dec": "26",
    "Jews2023_Jan-Apr": "27"
}

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


# LOGIN

group = ""
for row, item in link_groups.items():
    print(row)

while True:
    group = input("Choose one of these groups: ")
    if group in link_groups:
        break
    else: print("Invalid Option!")

driver = webdriver.Chrome()
driver.get("https://datathon.annotationportal.com/user/user_login")

#https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
def page_has_loaded(driver: webdriver.Chrome, sleep_time=2):
    def get_page_hash(driver: webdriver.Chrome):
        dom = driver.find_element(By.TAG_NAME, "html").get_attribute("innerHTML")
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    page_hash = 'empty'
    page_hash_new = ''
    
    while page_hash != page_hash_new: 
        page_hash = get_page_hash(driver)
        time.sleep(sleep_time)
        page_hash_new = get_page_hash(driver)

page_has_loaded(driver, 0)

signin = driver.find_element(By.NAME, "username")
signin.send_keys(USERNAME)

password = driver.find_element(By.NAME, "password")
password.send_keys(PASSWORD)

submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
driver.execute_script("arguments[0].click()", submit)

def main_tweet(driver: webdriver.Chrome):
    text = get_text(driver)
    check_language(driver, text)
    check_for_antisemitism(driver, text)

def get_text(driver: webdriver.Chrome) -> str:
    iframe = driver.find_element(By.ID, "twitter-widget-0")
    driver.switch_to.frame(iframe)
    tweet = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
    tweet_text = tweet.text # do while still accessible
    driver.switch_to.default_content()
    return tweet_text

def check_language(driver: webdriver.Chrome, text: str):
    if langdetect.detect(text) != "en":
       checkbox = driver.find_element(By.ID, "id_can_read")
       driver.execute_script("arguments[0].click()", checkbox)

def check_for_antisemitism(driver: webdriver.Chrome, text: str):
    antisemitism = driver.find_element(By.NAME, "antisemitism_rating")
    biased = CheckBiased(text)
    if biased <= 0.2:
        antisemitism.send_keys("Confident not antisemitic")
    elif biased > 0.2 and biased <= 0.4:
        antisemitism.send_keys("Probably not antisemitic")
    elif biased > 0.4 and biased <= 0.6:
        antisemitism.send_keys("I don't know")
    elif biased > 0.6 and biased <= 0.8:
        antisemitism.send_keys("Probably antisemitic")
    elif biased >= 0.8:
        antisemitism.send_keys("Confident antisemitic")

def check_content_type(driver: webdriver.Chrome) -> str:
    if len(driver.find_elements(By.CLASS_NAME, "r-1s2bzr4")) > 0:
        return "Attachment"
    elif len(driver.find_elements(By.TAG_NAME, "img")) > 1:
        return "Image"

num = 0
while True:
    driver.get(f"https://datathon.annotationportal.com/form/annotation/{link_groups[group]}/{num}")
    page_has_loaded(driver, 3)

    try:
        #Get Tweet Type
        main_tweet(driver)
    except NoSuchAttributeException:
        print("Tweet box not found.")

    try:
        tweet = driver.find_element(By.CLASS_NAME, "mdl-card__media")
        if tweet.text.find("The tweet cannot be found") != -1:
            print("Hello")
            checkbox = driver.find_element(By.NAME, "still_exists")
            driver.execute_script("arguments[0].click()", checkbox)
    except NoSuchAttributeException:
        print("Tweet was found")

    #Check if tweet is found
    break

while True: pass