import time

from scraper import Scraper

start = time.time()

company = Scraper(
    'Company', 'https://company.com/')

data = company.start()

company.checkRobots()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
