import sys
from src.vector_store import VectorStore

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query.py 'your query here'")
        return

    query_text = sys.argv[1]
    
    print(f"Query: {query_text}")
    print("-" * 30)

    try:
        store = VectorStore(collection_name="rag_pipeline")
        results = store.query(query_text, n_results=3)
        
        if not results:
            print("No results returned.")
            return

        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        for i in range(len(documents)):
            print(f"\nResult {i+1} (Distance: {distances[i]:.4f}):")
            print(f"Content: {documents[i][:200]}...")
            print(f"Metadata: {metadatas[i]}")

    except Exception as e:
        print(f"Error querying: {e}")

if __name__ == "__main__":
    main()
