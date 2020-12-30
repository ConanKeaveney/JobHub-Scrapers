import time

from scraper import Scraper

start = time.time()

googleEngineering = Scraper(
    'Google', 'https://careers.google.com/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&company=Google&company=YouTube&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&sort_by=date', "Engineering")

googleSales = Scraper(
    'Google', 'https://careers.google.com/jobs/results/?company=Google&company=Google%20Fiber&company=YouTube&employment_type=FULL_TIME&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&q=Sales&sort_by=date', "Sales")

data = googleEngineering.start() + googleSales.start()

print("Total Num Data Items:", len(data))


end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds), "to run"
print(end)
