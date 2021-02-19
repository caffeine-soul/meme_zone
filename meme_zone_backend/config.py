import os
import configparser
import pymongo

config = configparser.ConfigParser()
config.read("config.ini")

mongo_str = "mongodb+srv://{uname}:{password}@cluster0.63mup.mongodb.net/{dbname}?retryWrites=true&w=majority".format(uname=config["mongodb"]["username"], password=config["mongodb"]["password"], dbname=config["mongodb"]["dbname"])
mongo_client = pymongo.MongoClient(mongo_str)
db = mongo_client[config["mongodb"]["dbname"]]