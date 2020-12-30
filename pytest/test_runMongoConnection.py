from pprint import pprint

from pymongo import MongoClient

from ..connect import Connect

client = Connect.get_connection()

db = client.scrapers

#Insert
# db.test.insert_one(
#     {"item": "canvas",
#      "qty": 100,
#      "tags": ["cotton"],
#      "size": {"h": 28, "w": 35.5, "uom": "cm"}})

# print("Entry Added")

#Find
# cursor = db.test.find({"size.h": {"$lt": 30}})
# for inventory in cursor:
#      pprint(inventory)
