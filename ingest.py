import os
from pymongo import MongoClient
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from utils import build_text
from bson import ObjectId

# Load .env variables
load_dotenv()

# ---------------------------
# MONGO CONNECTION
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# ❗ Do NOT use get_default_database()
# Instead manually select DB
db_name = os.getenv("MONGO_DB", "mmrdb")   # fallback "mmrdb"
db = client[db_name]

# ---------------------------
# LOAD ML MODEL
# ---------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------
# CHROMADB SETUP
# ---------------------------
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("mmr_statistics")

# ---------------------------
# FETCH CHART DATA
# ---------------------------
def fetch_chart(chart_id):
    if not chart_id:
        return None
    if isinstance(chart_id, str):
        chart_id = ObjectId(chart_id)
    return db.charts.find_one({"_id": chart_id})

# ---------------------------
# FETCH STATISTICS
# ---------------------------
stats = list(db.statistics.find({"status": "published"}).limit(100))
print(f"Found {len(stats)} stats")

# ---------------------------
# PROCESS & INGEST
# ---------------------------
for s in stats:
    chart = fetch_chart(s.get("chartId"))

    # Build text block for embedding
    text = build_text(s, chart)

    # Compute embedding
    emb = model.encode(text).tolist()

    # Clean metadata (NO duplicates!)
    metadata = {
        "statisticId": str(s["_id"]),
        "title": s.get("title", ""),
        "region": s.get("region", ""),
        "industryId": str(s.get("industryId", "")),
        "isPremium": s.get("isPremium", False),
        "accessTier": s.get("accessTier", ""),
        "chart_type": chart.get("chartType") if chart else "",
        "chart_preview": chart.get("previewUrl") if chart else "",
    }

    # Upsert into Chroma
    collection.upsert(
        ids=[str(s["_id"])],
        documents=[text],
        metadatas=[metadata],
        embeddings=[emb]
    )

print("Ingestion complete.")
print("Chroma count:", collection.count())
