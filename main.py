# from dotenv import load_dotenv
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pickle

from pkg.read_urls import get_urls


# globals
COOKIE_PATH = "data/cookies.txt"

username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')

# init driver
driver = webdriver.Chrome()


# TODO: not working for some reason
# load cookies
# if os.path.exists(COOKIE_PATH):
#     with open(COOKIE_PATH, "rb") as f:
#         cookies = pickle.load(f)
#         for cookie in cookies:
#             driver.add_cookie(cookie)


# login to linkedin
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)
time.sleep(1.5)

# TODO: not working for some reason
# save cookies
# with open(COOKIE_PATH, "wb") as f:
#     pickle.dump(driver.get_cookies(), f)

# load list of urls from urls.txt
urls = get_urls()


# go to each of the url pages
for i, url in enumerate(urls):
    driver.get(url)
    time.sleep(3)

    # click "see more"
    driver.find_element_by_css_selector("#ember39 > span").click()

    # parse data from page
    details = driver.find_element_by_id("job-details").text
    title = driver.find_element_by_css_selector("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > h1").text
    company = driver.find_element_by_css_selector("#ember38").text
    location = driver.find_element_by_css_selector("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > div.mt2 > span.jobs-unified-top-card__subtitle-primary-grouping.mr2.t-black > span.jobs-unified-top-card__bullet").text

    # write to file
    with open(f"data/jobs/{i}.txt", 'w') as f:
        f.write(f"{url}\n")
        f.write(f"{title}\n")
        f.write(f"{company}\n")
        f.write(f"{location}\n")
        f.write(details)

# close session
driver.close()
