# from dotenv import load_dotenv
import os
import time
from string import Template
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from markdownify import markdownify

from pkg.read_urls import get_urls
from obsidian.core import Obsidian


# globals
COOKIE_PATH = "data/cookies.txt"
JOB_POST_NOTE_PATH = "data/job_search/job_descriptions/"
COMPANY_NOTE_PATH = "data/job_search/companies/"

username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')

# init drivers
driver = webdriver.Chrome()
obsidian = Obsidian("~/obsidian-main")


# login to linkedin
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)
time.sleep(1.5)


# load list of urls from urls.txt
urls = get_urls()


# go to each of the url pages
for i, url in enumerate(urls):
    driver.get(url)
    time.sleep(3)

    # click "see more"
    driver.find_element_by_css_selector("#ember38").click()

    # parse data from page
    job_dict = {
        "body": driver.find_element_by_id("job-details").get_attribute('innerHTML'),
        "title": driver.find_element_by_css_selector("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > h1").text,
        "company": driver.find_element_by_css_selector("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > div.mt2 > span.jobs-unified-top-card__subtitle-primary-grouping.mr2.t-black > span:nth-child(1)").text,
        "location": driver.find_element_by_css_selector("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > div.mt2 > span.jobs-unified-top-card__subtitle-primary-grouping.mr2.t-black > span.jobs-unified-top-card__bullet").text,
        "date": str(datetime.today().date()),
        "tags": " ".join(["#job"]),
        "url": url
    }

    job_dict["title"] = job_dict["title"].replace("/", "_")
    job_dict["body"] = markdownify(job_dict["body"])

    with open('job_description_template.md', 'r') as f:
        src = Template(f.read())
        job_dict["body"] = src.substitute(job_dict)

    # create company note if not exists
    try:
        obsidian.new_note(
            note_path=COMPANY_NOTE_PATH,
            title=job_dict["company"],
            body=f"**Date Pulled:** {datetime.today().date()}",
            tags=["#company"],
            overwrite=False,
            autolink_notes=False
        )
    except ValueError:
        print("Note already exists")
    

    obsidian.new_note(
        note_path=JOB_POST_NOTE_PATH,
        title=job_dict["title"],
        body=job_dict["body"],
        overwrite=True,
        autolink_notes=True
    )

# close session
driver.close()
