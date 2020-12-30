import time

from scraper import Scraper

start = time.time()

facebook = Scraper(
    'Facebook', 'https://www.facebook.com/careers/jobs/?page=1&results_per_page=100&offices[0]=Dublin%2C%20Ireland#search_result')

data = facebook.start()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
