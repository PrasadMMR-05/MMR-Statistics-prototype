from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# Option 1: use DB name from URI (recommended)
# db = client.get_default_database()

# Option 2 (if you want manual name)
db = client["mmr"]
