import json
import re

import requests
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, company, url):
        self.company = company
        self.url = url

    def scrape(self):

        url = requests.get(self.url)  # company career url

        # beautiful soup instance
        soup = BeautifulSoup(url.content, 'html.parser')

        # find script tag containing relevant data
        script = soup.find('script', {'type': 'text/javascript'})

        p = str(script.contents)  # convert script content to string

        p1 = p.split('"data":{"jobs":')

        p2 = p1[1].split(',"aggregations"')  # cut down to just relevant json

        escaped = p2[0].replace("\\", "")
        escaped2 = escaped.replace("https://", "")

        data = json.loads(escaped2)  # convert to python dictionary

        # reformatted data being stored here
        data2 = [dict() for x in range(len(data))]

        for i in range(len(data)):
            if data[i]['location'] == "Dublin, Ireland" and "Technology" in data[i]['category']:
                data2[i]['title'] = data[i]['title']
                data2[i]['location'] = "Dublin"
                data2[i]['category'] = data[i]['category']
                data2[i]['post date'] = data[i]['postedDate']
                data2[i]['description'] = data[i]['descriptionTeaser'] + "..."
                data2[i]['experience'] = data[i]['type']
                url = 'https://careers.sig.com/job/' + data[i]['jobSeqNo']
                data2[i]['url'] = url
                data2[i]['company'] = self.company
                print(data[i]['descriptionTeaser'] + "...")

        for i in range(len(data)):
            print(data[i]['location'])  # print all job titles

        data3 = [x for x in data2 if x != {}]

        end = 'scraper for ' + self.company + \
            ' finished running and returned ' + str(len(data3)) + ' items.'

        print(end)
        return data3
