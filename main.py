# from dotenv import load_dotenv
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pickle

from pkg.read_urls import get_urls

# load_dotenv()

if os.path.exists("data/cookies.txt"):
    # load cookies
    pass

username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')

driver = webdriver.Chrome()


# login to linkedin
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)
time.sleep(1.5)

# save cookies
with open("./data/cookies.txt", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

# load list of urls from urls.txt
urls = get_urls()


# go to each of the url pages
for url in urls:
    driver.get(url)
    time.sleep(3)

    # parse data from page

    # write to file


# close session
driver.close()
