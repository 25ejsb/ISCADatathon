from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchAttributeException
from time import sleep as wait
# if on mac, do brew install chromedriver

# use virtualenv to create enviornment

driver = webdriver.Chrome()
driver.get("https://x.com/login")

wait(3)

signin = driver.find_element(By.CSS_SELECTOR, "input")
signin.send_keys("hello")

while True:
    pass