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
        for i in range(20):
            offset = 10*i
            newUrl = self.addParam(self.url, 'offset', offset)
            curLen = len(data)
            data = self.scrape(newUrl, data)

            if (len(data) == curLen):
                print('Done')
                break
        print(len(data))
        return data

    def scrape(self, url, data):
        env_path = Path(__file__).resolve().parents[1] / 'util' / '.env'
        load_dotenv(dotenv_path=env_path)
        CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER")

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)
        driver.get(url)

        try:
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'job-tile')))
            print("Page is ready!")
        except TimeoutException:
            return data

        plain_text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(plain_text, 'html.parser')

        jobs = soup.findAll('div', {'class': 'job-tile'})
        if (len(jobs) == 0):
            return data

        for each in jobs:

            print('*********************************************************')

            job = {}

            title = each.find(
                'h3', {'class': 'job-title'}).contents[0]
            link = "https://amazon.jobs" + str(each.find(
                'a', {'class': 'job-link'})['href'])
            category, description, experience = self.getJobPage(link)

            location = "Dublin"
            post_date = each.find(
                'h2', {'class': 'posting-date'}).contents[0]
            # description = str(each.find(
            #     'p', {'class': 'description col-12'}).contents[0])
            # description = description.replace("<span>", "")
            # description = description.replace("</span>", "...")
            print(title)
            print(link)
            print(location)
            print(category)
            print(post_date)
            print("***Description***")
            print(description)
            print("***Qualifications***")
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
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)

        driver.get(link)

        try:
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'association-content')))
            print("Page is ready!")

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            div = soup.findAll('div', {'class': 'association-content'})[-1]
            a = div.find('a')
            p = div.find('p')

            divDescription = soup.find('div', {'class': 'section description'})
            divQualifications = soup.findAll('div', {'class': 'section'})[1]

            pQualifications = divQualifications.find('p').contents
            pDescription = divDescription.find('p').contents

            pQualificationsStr = [str(i) for i in pQualifications]
            pDescriptionStr = [str(i) for i in pDescription]

            pQualificationsClean = self.cleanhtml(
                str("\n".join(pQualificationsStr)))
            pDescriptionClean = self.cleanhtml(
                str("\n".join(pDescriptionStr)))

            if a is None:
                return p.contents[0], pDescriptionClean, pQualificationsClean
            return a.contents[0], pDescriptionClean, pQualificationsClean

        except:
            return "Unknown", "Unknown", "Unknown"

    # remove html tags
    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
