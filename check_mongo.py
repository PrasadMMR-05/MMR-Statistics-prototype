from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["mmr-statistics"]

print("Collections in MongoDB:")
for c in db.list_collection_names():
    print("-", c)

print("\nStatistics collection count:", db["marketstatistics"].count())
                            