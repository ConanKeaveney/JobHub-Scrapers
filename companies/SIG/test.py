from scraper import Scraper

sig = Scraper('sig', 'https://careers.sig.com/search-results?keywords=dublin')

data = sig.scrape()

for i in range(len(data)):
    print(data[i]['title'])
    print(data[i]['location'])
