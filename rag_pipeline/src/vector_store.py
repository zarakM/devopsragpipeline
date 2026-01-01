import os
import logging
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, collection_name: str = "rag_pipeline"):
        self.client = chromadb.PersistentClient(path="chroma_db")
        
        # Check for API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.warning("OPENAI_API_KEY not found. Embeddings will fail unless provided.")
            self.embedding_function = None
        else:
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def upsert(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return

        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            content = chunk["content"]
            metadata = chunk["metadata"]
            
            # Create a unique ID (simple hash or composite key)
            # Here we use a combination of file path/type index for simplicity, or just a uuid
            # For idempotency, a hash of the content + filepath is better
            import hashlib
            file_path = metadata.get("file_path", "unknown")
            chunk_hash = hashlib.md5((content + file_path).encode()).hexdigest()
            unique_id = f"{file_path}_{i}_{chunk_hash[:8]}"

            documents.append(content)
            
            # ChromaDB requires metadata values to be str, int, float, bool. 
            # We need to flatten complex dicts (like triggers list) or convert to str
            clean_metadata = {}
            for k, v in metadata.items():
                if isinstance(v, (list, dict)):
                    clean_metadata[k] = str(v)
                elif v is None:
                    clean_metadata[k] = ""
                else:
                    clean_metadata[k] = v
            
            metadatas.append(clean_metadata)
            ids.append(unique_id)

        # Upsert to Chroma
        try:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logging.info(f"Upserted {len(documents)} chunks to ChromaDB.")
        except Exception as e:
            logging.error(f"Failed to upsert to ChromaDB: {e}")

    def query(self, query_text: str, n_results: int = 5):
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            logging.error(f"Query failed: {e}")
            return None
