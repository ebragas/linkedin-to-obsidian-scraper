# from dotenv import load_dotenv
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# load_dotenv()

username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')

driver = webdriver.Chrome()


# login to linkedin
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)


# load list of urls from urls.txt
