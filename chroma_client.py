import chromadb
from config import settings

_client = None
_collection = None


def get_collection():
    """
    Returns (and creates if needed) the ChromaDB collection.
    Used by ingest.py
    """
    global _client, _collection

    if _collection is not None:
        return _collection

    _client = chromadb.PersistentClient(
        path=settings.CHROMA_PATH
    )

    _collection = _client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION_NAME
    )

    return _collection


def search_query(query: str, k: int = 5, filters: dict | None = None):
    collection = get_collection()

    where_clause = None

    # ✅ Build Chroma-compatible filter
    if filters:
        if len(filters) == 1:
            # Single filter is allowed directly
            key, value = next(iter(filters.items()))
            where_clause = {key: value}
        else:
            # Multiple filters MUST use $and
            where_clause = {
                "$and": [{k: v} for k, v in filters.items()]
            }

    results = collection.query(
        query_texts=[query],
        n_results=k,
        where=where_clause
    )

    response = []

    if not results or not results.get("ids"):
        return response

    for i in range(len(results["ids"][0])):
        response.append({
            "statisticId": results["metadatas"][0][i].get("statisticId"),
            "title": results["metadatas"][0][i].get("title"),
            "region": results["metadatas"][0][i].get("region"),
            "industryId": results["metadatas"][0][i].get("industryId"),
            "chart_type": results["metadatas"][0][i].get("chart_type"),
            "chart_preview": results["metadatas"][0][i].get("chart_preview"),
            "score": results["distances"][0][i]
        })

    return response
