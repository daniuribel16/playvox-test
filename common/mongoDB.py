from os import environ
from flask_pymongo import PyMongo, MongoClient

class MongoDb:
    def __init__(self, app, db_name):
        mongo_uri = environ['MONGO_URI'].replace('database_name', db_name)
        
        app.config["MONGO_URI"] = mongo_uri
        app.config["MONGO_DBNAME"] = db_name
        
        mongo = PyMongo(app)
        client = MongoClient(mongo_uri)
        
        self.db = client[db_name]
    
    def getDb(self):
        return self.db
