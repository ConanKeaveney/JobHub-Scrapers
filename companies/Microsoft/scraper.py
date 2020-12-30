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
        for i in range(5):
            urlOne = self.addParam(self.url, 's', i)
            fr = (20*i)
            urlTwo = self.addParam(urlOne, 'from', fr)
            curLen = len(data)
            print(urlTwo)
            data = self.scrape(urlTwo, data)

            if (len(data) == curLen):
                print('Done')
                break

            # data = self.scrape(url, data)
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
                EC.presence_of_element_located((By.CLASS_NAME, 'jobs-list-item')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
            return data

        plain_text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(plain_text, 'html.parser')

        jobs = soup.findAll('li', {'class': 'jobs-list-item'})
        if (len(jobs) == 0):
            return data

        for each in jobs:

            print('*********************************************************')

            job = {}

            link = each.find('a')['href']
            title = each.find('a')['data-ph-at-job-title-text']
            category = each.find('a')['data-ph-at-job-category-text']
            location = "Dublin"
            post_date = each.find(
                'span', {'class': 'job-date au-target'}).contents[0].strip()

            description, experience = self.getJobPage(link)

            print(link)
            print(title)
            print(location)
            print(category)
            print(post_date)
            print("***Description***")
            print(description)
            print("***Experience***")
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
                EC.presence_of_element_located((By.TAG_NAME, 'li')))
            print("Page is ready!")
            time.sleep(3)
        except TimeoutException:
            print("Loading took too much time!")
            return "Unknown", "Unknown"

        plain_text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(plain_text, 'html.parser')
        try:

            divDescription = soup.find(
                'div', {'class': 'job-description'}).contents
            divDescriptionStr = [str(i) for i in divDescription]
            divDescriptionClean = self.cleanhtml(
                str("\n".join(divDescriptionStr)))
        except:
            divDescriptionClean = "Unknown"

        try:

            divQualification = soup.findAll(
                'div', {'class': 'jd-info'})[-1]
            divQualificationStr = [str(i) for i in divQualification]
            divQualificationClean = self.cleanhtml(
                str("\n".join(divQualificationStr)))
        except:
            divQualificationClean = "Unknown"

        return divDescriptionClean, divQualificationClean

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>|<!--(.*?)-->')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
