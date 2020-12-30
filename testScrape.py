
import scrape

try:
    all = scrape.All()
    data = all.scrape()
except:
    print("Scrape Failed!!")
else:
    print("Scrape Success!!")
