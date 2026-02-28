from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

mongo_db = client["inventory_logs"]

logs_collection = mongo_db["login_logs"]