
import time

import scrape
from connect import Connect

start = time.time()


def get_mongo_db():
    client = Connect.get_connection()
    db = client.scrapers
    return db


try:
    all = scrape.All()
    data = all.scrape()
except:
    print("Scrape Failed")
else:
    mongodb = get_mongo_db()

    # empty db
    mongodb.test.delete_many({})

    # f = open("demofile.json", "a")
    # f.write(str(data))
    # f.close()
    for company, jobs in data.items():

        for job in jobs:

            mongodb.test.insert_one({"job": job})

    print("Operation Success")

    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)

    end = "Scraper took", "{:0>2}:{:0>2}:{:05.2f}".format(
        int(hours), int(minutes), seconds), "to run"

    print(end)
