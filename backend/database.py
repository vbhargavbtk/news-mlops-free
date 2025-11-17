from pymongo import MongoClient
from backend.config import settings

class DB:
    client: MongoClient = None

db = DB()

def get_db():
    return db.client[settings.DB_NAME]

def connect_to_mongo():
    print("Connecting to MongoDB...")
    db.client = MongoClient(settings.MONGO_URI)
    print("Connected to MongoDB.")

def close_mongo_connection():
    db.client.close()
    print("MongoDB connection closed.")
