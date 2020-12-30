import json
import os
import re
import time
import urllib.parse
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

    def start(self):
        data = []
        for i in range(1, 100):

            url = self.url
            params = {'page': i}

            url_parts = list(urllib.parse.urlparse(url))
            query = dict(urllib.parse.parse_qsl(url_parts[4]))
            query.update(params)

            url_parts[4] = urllib.parse.urlencode(query)
            newUrl = urllib.parse.urlunparse(url_parts)
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
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'p')))
            print("Page is ready!")
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
            return data
        try:
            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            div = soup.find('div', {'id': 'react-root-directory'})
            a = div.findAll('a', {'class': 'sc-bdVaJa bKWNxX'})
            print(len(a))
            if (len(a) == 0):
                return data

            for each in a:  # iterate over loop [above sections]
                # try:

                print('*********************************************************')

                job = {}
                link = "https://hubspot.com"+str(each.find('a')['href'])
                title = each.find(
                    'p', {'class': 'sc-htpNat iUzPVU'}).contents[0]
                category = each.find(
                    'p', {'class': 'sc-bxivhb hGgDVc'}).contents[0]
                location = "Dublin"
                print(title)
                print(category)
                print(link)
                description, experience = self.getJobPage(link)
                print(description)
                job['company'] = self.company
                job['title'] = title
                job['location'] = location
                job['category'] = category
                job['post_date'] = "Unknown"
                job['description'] = description
                job['experience'] = experience
                job['url'] = link

                data.append(job)
                # except:
                #     print("Job Error")

            end = 'scraper for ' + self.company + \
                ' finished running on this page and returned ' + \
                str(len(data)) + ' items.'

            print(end)

            return data

        except:
            print("General Exception")
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
                EC.presence_of_element_located((By.TAG_NAME, 'p')))
            print("Page is ready!")
            time.sleep(1)

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            divDescription = soup.find(
                'div', {'class': 'sc-dNLxif fTmRMR'})

            divDescriptionStr = [str(i) for i in divDescription]
            divDescriptionClean = self.cleanhtml(
                str("\n".join(divDescriptionStr)))

            return divDescriptionClean, "Unknown"

        except:
            print("Loading took too much time!")
            return "Unknown", "Unknown"

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
