import chromadb

# Same persistent path
client = chromadb.PersistentClient(
    path="C:/Users/UNIVERSAL COMPUTER/.antigravity/MMR/chroma_db"
)

# ---------------------------
# LIST COLLECTIONS
# ---------------------------
print("\nCollections found:")
for col in client.list_collections():
    print("-", col.name)

# ---------------------------
# GET mmr_statistics COLLECTION (✅ FIXED)
# ---------------------------
mmr = client.get_collection("mmr_statistics")

print("\n📊 mmr_statistics collection count:", mmr.count())

# ---------------------------
# SHOW SAMPLE RECORDS
# ---------------------------
results = mmr.get(limit=3)

print("\n--- SAMPLE MMR STATISTICS RECORDS ---")
for i, doc in enumerate(results["documents"]):
    print(f"\nRecord {i+1}")
    print("Document:\n", doc)
    print("Metadata:", results["metadatas"][i])
