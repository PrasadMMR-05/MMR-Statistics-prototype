import os
from typing import List, Dict, Any
from bson import ObjectId
import pymongo
from sentence_transformers import SentenceTransformer

from config import settings
from chroma_client import get_collection


# ---------------------------
# MONGO CONNECTION
# ---------------------------
def get_db():
    client = pymongo.MongoClient(settings.MONGODB_URI)
    return client[settings.DB_NAME]


# ---------------------------
# FETCH STATISTICS (REAL DATA)
# ---------------------------
def fetch_statistics(db, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetches statistics from MongoDB (REAL data).
    """
    collection = db[settings.COLLECTION_STATISTICS]

    # SAFE QUERY: fetch any documents
    stats = list(
        collection
        .find({})
        .limit(limit)
    )

    return stats


# ---------------------------
# FETCH CHART BY ID
# ---------------------------
def fetch_chart(db, chart_id) -> Dict[str, Any]:
    if not chart_id:
        return {}

    collection = db[settings.COLLECTION_CHARTS]

    try:
        if isinstance(chart_id, str):
            chart_id = ObjectId(chart_id)

        return collection.find_one({"_id": chart_id}) or {}

    except Exception as e:
        print(f"⚠️ Chart fetch error for chartId={chart_id}: {e}")
        return {}


# ---------------------------
# BUILD TEXT FOR EMBEDDING
# ---------------------------
def format_statistic_text(stat: Dict[str, Any], chart: Dict[str, Any]) -> str:
    title = stat.get("title", "")
    description = stat.get("description", "")
    region = stat.get("region", "Global")
    industry = str(stat.get("industryId", ""))
    time_period = stat.get("timePeriod", "")

    chart_type = chart.get("chartType", "Unknown")

    # Series names
    series = chart.get("series", [])
    series_names = ", ".join(
        s.get("name", "Unnamed") for s in series if isinstance(s, dict)
    )

    x_label = chart.get("xAxisLabel", "")
    y_label = chart.get("yAxisLabel", "")

    text = f"""
{title}
Region: {region}
Industry: {industry}
Time Period: {time_period}

Description:
{description}

Chart:
Type: {chart_type}
Series: {series_names}
X-axis: {x_label}
Y-axis: {y_label}
""".strip()

    return text


# ---------------------------
# INGESTION PIPELINE
# ---------------------------
def run_ingestion():
    print("\n--- Starting Ingestion Process ---")

    # 1. Connect to MongoDB
    db = get_db()
    print(f"✅ Connected to MongoDB database: {settings.DB_NAME}")

    # 2. Fetch statistics
    stats = fetch_statistics(db, limit=100)
    print(f"📊 Fetched {len(stats)} statistics")

    if not stats:
        print("❌ No statistics found. Exiting.")
        return

    # 3. Load embedding model
    print(f"🤖 Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    documents = []
    metadatas = []
    ids = []

    # 4. Process each statistic
    print("🔄 Processing statistics and joining charts...")
    for stat in stats:
        stat_id = str(stat["_id"])
        chart_id = stat.get("chartId")

        chart = fetch_chart(db, chart_id)
        text = format_statistic_text(stat, chart)

        metadata = {
            "statisticId": stat_id,
            "title": stat.get("title", ""),
            "region": stat.get("region", ""),
            "industryId": str(stat.get("industryId", "")),
            "isPremium": bool(stat.get("isPremium", False)),
            "accessTier": stat.get("accessTier", ""),
            "chart_type": chart.get("chartType", ""),
            "chart_preview": chart.get("previewUrl", "")
        }

        documents.append(text)
        metadatas.append(metadata)
        ids.append(stat_id)

    # 5. Generate embeddings
    print(f"🧠 Generating embeddings for {len(documents)} documents...")
    embeddings = model.encode(documents).tolist()

    # 6. Store in ChromaDB
    print("📦 Storing embeddings in ChromaDB...")
    collection = get_collection()

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"✅ Successfully ingested {len(ids)} records into ChromaDB")
    print("--- Ingestion Complete ---\n")


if __name__ == "__main__":
    run_ingestion()
