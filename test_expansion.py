import sys
import os

# Adjust path
sys.path.append(os.getcwd())

from generate import RAGService

def test():
    print("Initializing RAG Service...")
    rag = RAGService()
    
    queries = [
        "mobile trends",
        "EV sales growth",
        "healthcare in Asia"
    ]

    for q in queries:
        print(f"\nQuery: {q}")
        keywords = rag.expand_query(q)
        print(f"Keywords: {keywords}")
        print("-" * 20)

if __name__ == "__main__":
    test()
