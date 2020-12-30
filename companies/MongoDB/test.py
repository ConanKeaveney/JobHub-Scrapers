from scraper import Scraper

mongodb = Scraper(
    'MongoDB', 'https://www.mongodb.com/careers/locations/dublin')

data = mongodb.scrape()
# mongodb.checkRobots()
