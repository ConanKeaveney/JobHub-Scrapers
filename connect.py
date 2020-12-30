from pymongo import MongoClient

class Connect(object):
    @staticmethod    
    def get_connection():
        return MongoClient("mongodb+srv://user:8b9ax1puyPu8RUzQ@cluster0-ctwix.mongodb.net/test?retryWrites=true&w=majority")