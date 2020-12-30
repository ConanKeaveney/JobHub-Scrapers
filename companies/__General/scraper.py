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

    def checkRobots(self):
        import os
        result = os.popen("curl https://www.company.com/robots.txt").read()
        result_data_set = {"Disallowed": [], "Allowed": []}

        for line in result.split("\n"):
            if line.startswith('Allow'):    # this is for allowed url
                result_data_set["Allowed"].append(line.split(': ')[1].split(
                    ' ')[0])    # to neglect the comments or other junk info
            elif line.startswith('Disallow'):    # this is for disallowed url
                result_data_set["Disallowed"].append(line.split(': ')[1].split(
                    ' ')[0])    # to neglect the comments or other junk info

        print(result_data_set)

    def start(self):
        data = []
        for i in range(1, 20):
            # change 'page' for whatever tracks pages in the url
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
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # used if jobs can only be seen when js loads
        driver = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        driver.set_window_size(1440, 900)
        driver.get(url)
        try:
            myElem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'association-content')))
            print("Page is ready!")

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            # class for each job item
            jobs = soup.findAll('li', {'class': 'search-result job-listing'})
            if (len(jobs) == 0):
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
                description = 'Unknown'
                experience = 'Unknown'
                print(title)
                print(link)
                print(location)
                print(category)
                print(post_date)
                print(description)
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
        except:
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
            myElem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'association-content')))
            print("Page is ready!")
            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            divDescription = soup.find('div', {'class': 'section description'})

            pDescription = divDescription.find('p').contents

            pDescriptionStr = [str(i) for i in pDescription]

            pDescriptionClean = self.cleanhtml(
                str("\n".join(pDescriptionStr)))

            return pDescriptionClean

        except:
            return "Unknown"

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>|<!--(.*?)-->')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
