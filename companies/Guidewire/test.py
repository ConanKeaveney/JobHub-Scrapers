import time

from scraper import Scraper

start = time.time()

guidewire = Scraper(
    'Guidewire', 'https://careers.guidewire.com/job_search?dept=all&loc=dublin')

data = guidewire.start()


end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
