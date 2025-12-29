from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["mmr-statistics"]

print("Total statistics count:", db["statistics"].count_documents({}))
