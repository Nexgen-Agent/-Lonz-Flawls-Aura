# backend/database/connection.py

from pymongo import MongoClient
from backend.config import settings

class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()

    def get_collection(self, name):
        return self.db[name]

# In a real application, you'd want to manage the client's lifecycle
# (e.g., closing it gracefully), but for this example, a singleton is fine.
db_client = MongoClient(settings.DATABASE_URL)
db = db_client.get_database("aura_main")

def get_db():
    return db
