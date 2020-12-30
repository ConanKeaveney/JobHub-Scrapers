import time

from scraper import Scraper

start = time.time()

amazon = Scraper(
    'Amazon', 'https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&cities[]=Dublin%2C%20IRL&distanceType=Mi&radius=Anykm&latitude=53.34807&longitude=-6.24827&loc_group_id=&loc_query=Dublin%2C%20Ireland&base_query=&city=Dublin&country=IRL&region=&county=County%20Dublin&query_options=&')

data = amazon.start()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
