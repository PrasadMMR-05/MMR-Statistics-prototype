import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = "mmr-statistics"

    # REAL collections (confirmed)
    COLLECTION_STATISTICS = "statistics"
    COLLECTION_CHARTS = "charts"

    # ChromaDB
    CHROMA_PATH = "./chroma_db"
    CHROMA_COLLECTION_NAME = "mmr_statistics"

    # Embedding model
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

settings = Settings()
