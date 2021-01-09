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

    def checkRobots(self):
        import os
        result = os.popen("curl https://www.mongodb.com/robots.txt").read()
        result_data_set = {"Disallowed": [], "Allowed": []}

        for line in result.split("\n"):
            if line.startswith('Allow'):    # this is for allowed url
                result_data_set["Allowed"].append(line.split(': ')[1].split(
                    ' ')[0])    # to neglect the comments or other junk info
            elif line.startswith('Disallow'):    # this is for disallowed url
                result_data_set["Disallowed"].append(line.split(': ')[1].split(
                    ' ')[0])    # to neglect the comments or other junk info

        print(result_data_set)

    def fix_JSON(self, json_message):
        result = None
        try:
            result = json.loads(json_message)
        except Exception as e:
            # Find the offending character index:
            idx_to_replace = int(str(e).split(' ')[-1].replace(')', ''))
            # Remove the offending character:
            json_message = list(json_message)
            json_message[idx_to_replace] = ' '
            new_message = ''.join(json_message)
            return self.fix_JSON(new_message)
        return result

    def scrape(self):

        url = requests.get(self.url)  # company career url

        # beautiful soup instance
        soup = BeautifulSoup(url.content, 'html.parser')

        # find script tag containing relevant data
        script = soup.find(
            'script', {'id': 'data-grnhs', 'type': 'text/template'})

        p = str(script.contents)  # convert script content to string

        p1 = p.split(',"jobs":')

        p2 = p1[1].split(']')

        # data = json.loads(p1[1])  # convert to python dictionary
        p2[0] += ']'

        data = self.fix_JSON(p2[0])  # convert to python dictionary

        # reformatted data being stored here
        data2 = [dict() for x in range(len(data))]

        for i in range(len(data)):
            if "Dublin" in data[i]['location']:

                data2[i]['title'] = data[i]['title']
                data2[i]['location'] = data[i]['location']
                data2[i]['category'] = data[i]['department']
                data2[i]['post date'] = 'Unknown'
                data2[i]['experience'] = 'Unknown'
                url = 'https://www.mongodb.com/careers/jobs/' + \
                    str(data[i]['id'])
                data2[i]['url'] = url
                data2[i]['description'] = self.getJobPage(url)
                data2[i]['company'] = self.company

        for i in range(len(data)):
            print("*************************************")
            print(data[i]['title'])  # print all job titles

        data3 = [x for x in data2 if x != {}]

        end = 'scraper for ' + self.company + \
            ' finished running and returned ' + str(len(data3)) + ' items.'

        print(end)
        return data3

    def getJobPage(self, link):
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

        driver.get(link)
        try:
            print(link)
            myElem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'p')))
            print("Page is ready!")
            plain_text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(plain_text, 'html.parser')

            div = soup.find(
                'div', {'class': 'w-max-600 job-column job-description'})
            divStr = [str(i) for i in div]
            divClean = self.cleanhtml(
                str("\n".join(divStr)))
            print("********************")
            print(divClean)
            return divClean

        except:
            print("Job Page Error")
            return "Unknown"

    def cleanhtml(self, raw_html):
        cleanr = re.compile('</h2>|</li>|</p>')
        cleantext = re.sub(cleanr, '\n', raw_html)

        cleanr2 = re.compile('<.*?>|<!--(.*?)-->')
        cleantext2 = re.sub(cleanr2, '', cleantext)
        return cleantext2
