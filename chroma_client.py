import chromadb

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("mmr_statistics")

def search_query(query, k=5, allowed_industries=None):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    items = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        
        # server-side industry filter (basic)
        if allowed_industries and meta["industryId"] not in allowed_industries:
            continue

        items.append({
            "statisticId": meta["statisticId"],
            "title": meta["title"],
            "industryId": meta["industryId"],
            "isPremium": meta["isPremium"],
            "accessTier": meta["accessTier"],
            "chartType": meta.get("chart_type"),
        })

    return items[:k]
