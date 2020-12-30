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

        data = self.scrape(self.url, data)

        print('Done')

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
                EC.presence_of_element_located((By.XPATH, '//button[@class="js-listjs-pagination-next listjs-pagination-next"]')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
            return []

        for i in range(1, 100):
            if (i > 1):
                try:
                    btn = driver.find_element_by_xpath(
                        '//button[@class="js-listjs-pagination-next listjs-pagination-next"]')
                    driver.execute_script("arguments[0].click();", btn)
                except:
                    break
            time.sleep(1)
            plain_text = driver.page_source

            soup = BeautifulSoup(plain_text, 'html.parser')

            jobs = soup.findAll(
                'li', {'data-location': 'dublin-ireland'})

            if ((len(jobs) == 0)):
                break

            for each in jobs:

                print('*********************************************************')

                job = {}

                # location = str(each['data-location'])
                location = "Dublin"
                title = str(each.find(
                    'a', {'class': 'jobs-list__name-link'}).contents[0])
                link = "https://careers.guidewire.com" + str(each.find(
                    'a', {'class': 'jobs-list__name-link'})['href'])
                category, description, experience = self.getJobPage(link)

                post_date = 'Unknown'
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

        driver.quit()

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
                EC.presence_of_element_located((By.CLASS_NAME, 'c-job-description')))
            print("Page is ready!")

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            liCategory = soup.find(
                'li', {'class': 'u-pt--1 u-pb--1'})
            strongCategory = liCategory.find(
                'strong').contents[0]
            print(strongCategory)

            divDescription = soup.find(
                'div', {'class': 'c-job-description'})
            divDescriptionStr = [str(i) for i in divDescription]
            divDescriptionClean = self.cleanhtml(
                str("\n".join(divDescriptionStr)))

            return strongCategory, divDescriptionClean, "Unknown"

        except:
            print("Loading took too much time!")
            return "Unknown", "Unknown", "Unknown"

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
