from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from CheckBiased import CheckBiased
import os, time, langdetect, ollama

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

ihra_sections = [
    "1.0 - Hatred Towards Jews",
    "3.1.1 - Justifying harming of Jews in the name of a radical ideology",
    "3.1.2 - Mendacious or stereotypical allegations about Jews as such + Jewish power",
    "3.1.3 - Blaming the Jews as a people for what a single person or group has done",
    "3.1.4 - Denying the fact, scope, mechanisms or intentionality of the Holocaust",
    "3.1.5 - Accusing the Jews/Israel of inventing or exaggerating the Holocaust.",
    "3.1.6 - Accusing Jews of being more loyal to Israel, or to 'Jewish priorities'",
    "3.1.7 - Denying the Jewish people right to self-determination, e.g., 'Israel is racist per se'",
    "3.1.8 - Applying double standards to Israel (sth. that is not expected of other nations)",
    "3.1.9 - Classic antisemitism (e.g. blood libel) to characterize Israel or Israelis.",
    "3.1.10 - Drawing comparisons of contemporary Israeli policy to that of the Nazis",
    "3.1.11 - Holding Jews collectively responsible for actions of the state of Israel",
    "None"
]

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
    driver.find_element(By.NAME, "content_type").send_keys(check_content_type(driver))
    driver.find_element(By.NAME, "sentiment_rating").send_keys(check_sentiment_rating(text))
    if distortion(text) == True:
        checkbox = driver.find_element(By.ID, "Distortion")
        driver.execute_script("arguments[0].click()", checkbox)
    if sarcasm(text) == True:
        checkbox = driver.find_element(By.ID, "sarcasm")
        driver.execute_script("arguments[0].click()", checkbox)
    driver.find_element(By.NAME, "calling_out").send_keys(calling_out(text))
    driver.find_element(By.NAME, "denying").send_keys(denying(text))
    driver.find_element(By.NAME, "holocaust").send_keys(holocaust(text))
    driver.find_element(By.TAG_NAME, "html").send_keys(Keys.ENTER)

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
       driver.find_element(By.TAG_NAME, "html").send_keys(Keys.ENTER)

def check_for_antisemitism(driver: webdriver.Chrome, text: str):
    antisemitism = driver.find_element(By.NAME, "antisemitism_rating")
    biased = CheckBiased(text)
    if biased <= 0.2:
        antisemitism.send_keys("Confident not antisemitic")
    elif biased > 0.2 and biased <= 0.4:
        antisemitism.send_keys("Probably not antisemitic")
        check_content_type(driver)
        driver.find_element(By.NAME, "IHRA_section").send_keys(check_ihra_section(text))
    elif biased > 0.4 and biased <= 0.6:
        antisemitism.send_keys("I don't know")
        check_content_type(driver)
        driver.find_element(By.NAME, "IHRA_section").send_keys(check_ihra_section(text))
    elif biased > 0.6 and biased <= 0.8:
        antisemitism.send_keys("Probably antisemitic")
        check_content_type(driver)
        driver.find_element(By.NAME, "IHRA_section").send_keys(check_ihra_section(text))
    elif biased >= 0.8:
        antisemitism.send_keys("Confident antisemitic")
        check_content_type(driver)
        driver.find_element(By.NAME, "IHRA_section").send_keys(check_ihra_section(text))

def check_ihra_section(text: str) -> str:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"From this python list: {ihra_sections}, and this text {text}, determine what category does the text fall into from the python list, and then just output the correct section, DONT GIVE ANY OTHER INFORMATION",
            },
        ],
    )
    return str(response["message"]["content"]).replace("'", "")

def check_content_type(driver: webdriver.Chrome) -> str:
    iframe = driver.find_element(By.ID, "twitter-widget-0")
    driver.switch_to.frame(iframe)
    if len(driver.find_elements(By.CSS_SELECTOR, "div.css-1dbjc4n.r-1ets6dv.r-1867qdf.r-1phboty.r-rs99b7.r-18u37iz.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg")) > 0 or len(driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="videoComponent"]')) > 0:
        driver.switch_to.default_content()
        return "Attachment"
    elif len(driver.find_elements(By.CSS_SELECTOR, "img.css-9pa8cd")) > 1 and not check_if_reply(driver) or check_if_reply(driver) and len(driver.find_elements(By.CSS_SELECTOR, "img.css-9pa8cd")) > 2:
        driver.switch_to.default_content()
        return "Image"
    else:
        driver.switch_to.default_content()
        return "Text"

def check_if_reply(driver: webdriver.Chrome) -> bool:
    if len(driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')) > 1:
        return True
    else: return False

def calling_out(text: str):
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"is this tweet calling out or reporting on antisemitism (including in the past but excluding the Holocaust. However, if Holocaust commemoration includes references to the present or future, such as 'never again,' calling out applies). Reply with 'True' or 'False', DONT GIVE ANY OTHER INFORMATION: {text}",
            },
        ],
    )
    return response["message"]["content"]

def denying(text: str):
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"is this Denying a reasonable accusation of antisemitism. Reply with 'True' or 'False', DONT GIVE ANY OTHER INFORMATION: {text}",
            },
        ],
    )
    return response["message"]["content"]

def holocaust(text: str):
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"is this tweet related to the Holocaust, Reply with 'True' or 'False', DONT GIVE ANY OTHER INFORMATION: {text}",
            },
        ],
    )
    return response["message"]["content"]

def check_sentiment_rating(text: str) -> int:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"Rate this tweet from 1 to 10 based on the sentiment, JUST GIVE THE RATING, NOTHING ELSE: {text}",
            },
        ],
    )
    score = int(response["message"]["content"])
    if score <= 0.1:
        return "Very Negative"
    elif score > 0.1 and score <= 0.4:
        return "Negative"
    elif score > 0.4 and score <= 0.7:
        return "I don't know"
    elif score > 0.7 and score <= 0.9:
        return "Positive"
    elif score >= 1:
        return "Very Positive"
    
def distortion(text: str) -> bool:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"is this Using imagery and language associated with the Holocaust for political, ideological, or commercial purposes unrelated to this history, Reply with 'True' or 'False', DONT GIVE ANY OTHER INFORMATION: {text}",
            },
        ],
    )
    return bool(response["message"]["content"])

def sarcasm(text: str) -> bool:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"is this tweet sarcastic, Reply with 'True' or 'False', DONT GIVE ANY OTHER INFORMATION: {text}",
            },
        ],
    )
    return bool(response["message"]["content"])

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
            checkbox = driver.find_element(By.NAME, "still_exists")
            driver.execute_script("arguments[0].click()", checkbox)
            driver.find_element(By.TAG_NAME, "html").send_keys(Keys.ENTER)
    except NoSuchAttributeException:
        print("Tweet was found")

    #Check if tweet is found