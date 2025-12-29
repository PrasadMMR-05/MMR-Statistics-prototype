import json
import ast
import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from chroma_client import get_collection
except ImportError:
    # If running from a different directory, try to adjust path or fail gracefully
    # Assuming running from the directory where chroma_client.py is located
    pass

def check_chroma():
    try:
        collection = get_collection()
        count = collection.count()
        print(f"\n[Stats] mmr_statistics collection count: {count}")

        if count == 0:
            print("No records found.")
            return

        print("\n--- SAMPLE MMR STATISTICS RECORDS ---\n")
        
        # Determine number of records to fetch
        n_results = min(count, 10)
        results = collection.get(limit=n_results)

        ids = results['ids']
        metadatas = results['metadatas']
        documents = results['documents']

        for i in range(len(ids)):
            print(f"Record {i+1}")
            print(f"ID: {ids[i]}")
            
            # Print Metadata
            if metadatas and i < len(metadatas):
                print(f"Metadata: {metadatas[i]}")
            
            # Print Document/Description as JSON String
            if documents and i < len(documents):
                doc_content = documents[i]
                
                # Check if it looks like a dict string
                if isinstance(doc_content, str) and doc_content.strip().startswith('{'):
                    try:
                        # Convert python string dict to actual dict
                        doc_dict = ast.literal_eval(doc_content)
                        # Convert dict to JSON formatted string
                        json_str = json.dumps(doc_dict, indent=2)
                        print("Description (JSON):")
                        print(json_str)
                    except Exception as e:
                        # Fallback
                        print(f"Description (Raw): {doc_content}")
                else:
                    print(f"Description: {doc_content}")
            
            print("-" * 40)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_chroma()
