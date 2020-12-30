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

    def __init__(self, company, url, category):
        self.company = company
        self.url = url
        self.category = category

    def start(self):
        data = []
        for i in range(1, 100):

            url = self.url
            param, newvalue = 'page', str(i)
            parsed = urlsplit(url)
            query_dict = parse_qs(parsed.query)
            query_dict[param][0] = newvalue
            query_new = urlencode(query_dict, doseq=True)
            parsed = parsed._replace(query=query_new)
            newUrl = (parsed.geturl())
            # print(query)
            # print(url)
            # print(newUrl)
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
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)
        driver.get(url)

        try:
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'search-results')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
            return data

        plain_text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(plain_text, 'html.parser')

        jobs = soup.find('ol', {'id': 'search-results'})

        if (len(jobs) == 0):
            return data

        for each in jobs:

            try:

                print('*********************************************************')
                job = {}
                link = "https://careers.google.com"+each.find('a')['href']
                title = each.find('a')['aria-label']
                description, experience = self.getJobPage(link)
                location = "Dublin"
                category = self.category
                print(title)
                print(link)
                print(description)
                print(experience)
                job['company'] = self.company
                job['title'] = title
                job['location'] = location
                job['category'] = category
                job['post_date'] = "Unknown"
                job['description'] = description
                job['experience'] = experience
                job['url'] = link

                data.append(job)
            except:
                print("Job Error")

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
                EC.presence_of_element_located((By.TAG_NAME, 'br')))
            print("Page is ready!")

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            divAbout = soup.find(
                'div', {'class': 'gc-job-detail__section gc-job-detail__section--description'}).contents
            divResponsibilities = soup.find(
                'div', {'class': 'gc-job-detail__section gc-job-detail__section--responsibilities'}).contents
            divAbout2 = divAbout + divResponsibilities
            aboutStr = [str(i) for i in divAbout2]
            aboutClean = self.cleanhtml(
                str("\n".join(aboutStr)))

            divQualifications = soup.find(
                'div', {'class': 'gc-job-qualifications gc-user-generated-content'}).contents
            qualificationsStr = [str(i) for i in divQualifications]
            qualificationsClean = self.cleanhtml(
                str("\n".join(qualificationsStr)))

            return aboutClean, qualificationsClean

        except:
            print("Loading took too much time!")
            return "Unknown", "Unknown"

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
