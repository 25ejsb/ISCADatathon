from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchAttributeException
# if on mac, do brew install chromedriver

driver = webdriver.Chrome()
driver.get("https://google.com")

while True:
    pass