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
            # print(newUrl)
            curLen = len(data)
            data = self.scrape(newUrl, data)

            # print(len(data))
            # print(curLen)
            # print((len(data) - curLen))
            # print(newUrl)

            # if num of jobs returned from page less than 25(max for page)
            if (len(data) == curLen or ((len(data) - curLen) < 100)):
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
                EC.presence_of_element_located((By.CLASS_NAME, '_8sef')))
            print("Page is ready!")
        except TimeoutException:
            return data
        try:

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            jobs = soup.findAll('a', {'class': '_8sef'})
            if (len(jobs) == 0):
                return data
            print("Num of jobs on page:", len(jobs))

            for each in jobs:

                print('*********************************************************')

                job = {}

                title = each.find(
                    'div', {'class': '_8sel _97fe'}).contents[0]
                link = "https://facebook.com" + str(each['href'])
                div = each.find(
                    'div', {'class': '_8sed'})
                category = div.find(
                    'div', {'class': '_8see _97fe'}).contents[0]

                description, experience = self.getJobPage(link)

                location = "Dublin"
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
                EC.presence_of_element_located((By.ID, 'careersPageContainer')))
            print("Page is ready!")

            time.sleep(1)

            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            divDescription = soup.find(
                'div', {'class': '_97fe _1n-_ _6hy- _94t2'}).contents
            divDescription2 = soup.find('div', {'class': '_8mlh'}).contents

            divDescriptionFinal = divDescription+divDescription2

            divDescriptionFinalStr = [str(i) for i in divDescriptionFinal]

            divDescriptionFinalStrClean = self.cleanhtml(
                str("\n".join(divDescriptionFinalStr)))

            # print(divDescriptionFinalStrClean)

            divQualifications = soup.findAll(
                'div', {'class': '_8mlh'})[1].contents

            divQualificationsFinal = divQualifications

            divQualificationsFinalStr = [str(i)
                                         for i in divQualificationsFinal]

            divQualificationsFinalStrClean = self.cleanhtml(
                str("\n".join(divQualificationsFinalStr)))
            # print(divQualificationsFinalStrClean)

            return divDescriptionFinalStrClean, divQualificationsFinalStrClean

        except:
            print("Loading took too much time!")
            return "Unknown", "Unknown"

    # remove html tags
    def cleanhtml(self, raw_html):
        cleanr = re.compile('<div class="_97fe _1n-z _6hy- _8lfs">')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<div class="_1zh- _8lfz">')
        cleantext2 = re.sub(cleanr2, '\n', cleantext)

        cleanr3 = re.compile('<.*?>')
        cleantext3 = re.sub(cleanr3, '', cleantext2)
        return cleantext3
