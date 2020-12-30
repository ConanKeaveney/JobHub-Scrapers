import time

from scraper import Scraper

start = time.time()

microsoft = Scraper(
    'Microsoft', 'https://careers.microsoft.com/us/en/search-results?qcity=Dublin&qstate=Dublin&qcountry=Ireland&from=0&s=0')

data = microsoft.start()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
