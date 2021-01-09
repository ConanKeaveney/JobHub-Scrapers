import json
import os
import re
import time
from pathlib import Path  # python3 only
from urllib.parse import parse_qs, urlencode, urlsplit

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Scraper:

    def __init__(self, company, url):
        self.company = company
        self.url = url

    def addParam(self, url, param, newvalue):
        param, newvalue = param, str(newvalue)
        parsed = urlsplit(url)
        query_dict = parse_qs(parsed.query)
        query_dict[param][0] = newvalue
        query_new = urlencode(query_dict, doseq=True)
        parsed = parsed._replace(query=query_new)
        newUrl = (parsed.geturl())
        return newUrl

    def start(self):
        data = []
        for i in range(1, 20):
            newUrl = self.addParam(self.url, 'page', i)
            print(newUrl)
            curLen = len(data)
            data = self.scrape(newUrl, data)

            if (len(data) == curLen):
                print('Done')
                break
        return data

    def scrape(self, url, data):
        env_path = Path(__file__).resolve().parents[1] / 'util' / '.env'
        load_dotenv(dotenv_path=env_path)
        CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER")

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-sandbox")
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)
        driver.get(url)

        try:
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h4')))
            print("Page is ready!")
        except TimeoutException:
            print("Timeout")
            return data

        plain_text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(plain_text, 'html.parser')

        jobs = soup.findAll('li', {'class': 'search-result job-listing'})
        if (len(jobs) == 0):
            print("No Jobs")
            return data
        print(len(jobs))

        for each in jobs:

            print('*********************************************************')

            job = {}

            title = str(each.find(
                'a', {'class': 'job-listing__link'}).contents[0])
            link = str(each.find(
                'a', {'class': 'job-listing__link'})['href'])
            category = str(each.find(
                'span', {'class': 'job-listing__department eyebrow'}).contents[0])

            location = "Dublin"
            post_date = str(each.find(
                'span', {'class': 'job-listing__created'}).contents[0])
            description, experience = self.getJobPage(link)
            print(title)
            print(link)
            print(location)
            print(category)
            print(post_date)
            print(description)
            print(experience)
            job['company'] = self.company
            job['title'] = title
            job['location'] = location
            job['category'] = category
            job['post_date'] = post_date
            job['description'] = description
            job['experience'] = experience
            job['url'] = link

            data.append(job)

        end = 'scraper for ' + self.company + \
            ' finished running and returned ' + str(len(data)) + ' items.'

        print(end)
        return data

    def getJobPage(self, link):
        CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER")

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-sandbox")
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)

        driver.get(link)

        try:
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'job-description')))
            print("Page is ready!")

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            divDescription = soup.find(
                'div', {'class': 'job-description'}).contents
            divQualifications = soup.find(
                'div', {'class': 'qualification grid'}).contents

            QualificationsStr = [str(i) for i in divQualifications]
            DescriptionStr = [str(i) for i in divDescription]

            QualificationsClean = self.cleanhtml(
                str("\n".join(QualificationsStr)))
            DescriptionClean = self.cleanhtml(
                str("\n".join(DescriptionStr)))

            return DescriptionClean, QualificationsClean

        except:
            print("Exception")
            return "Unknown", "Unknown"

    # remove html tags
    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
