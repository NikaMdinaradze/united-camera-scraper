from pymongo import MongoClient
import os

MONGO_USERNAME = os.getenv("DATABASE_USERNAME")
MONGO_PASSWORD = os.getenv("DATABASE_PASSWORD")
MONGO_HOST = os.getenv("DATABASE_HOST")
MONGO_PORT = os.getenv("DATABASE_PORT")

uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(uri)

db = client['development']

collection = db['cameras']
