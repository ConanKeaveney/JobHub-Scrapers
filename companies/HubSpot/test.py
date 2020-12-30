import time

from scraper import Scraper

start = time.time()

hubspot = Scraper(
    'HubSpot', 'https://www.hubspot.com/careers/jobs?hubs_signup-url=www.hubspot.com/careers/dublin-ireland&hubs_signup-cta=careers-location-bottom&page=1#office=dublin;')

data = hubspot.start()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
