from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchAttributeException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time, os

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

num = 0
while True:
    driver.get(f"https://datathon.annotationportal.com/form/annotation/{link_groups[group]}/{num}")
    page_has_loaded(driver, 2)
    iframe = driver.find_element(By.ID, "twitter-widget-0")
    driver.switch_to.frame(iframe)
    tweet = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
    print(tweet.text)
    break

while True: pass