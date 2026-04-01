import chromadb
from chromadb.config import Settings
import logging
import uuid

logger = logging.getLogger(__name__)

class LongTermMemory:
    """Vector-based memory for long-term storage and retrieval of interactions."""
    def __init__(self, collection_name: str = "agent_memory"):
        # For simplicity, using persistent local storage
        try:
            self.client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.client.get_or_create_collection(name=collection_name)
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.collection = None

    def store_memory(self, session_id: str, text: str, metadata: dict = None):
        if not self.collection:
            return
        doc_id = f"{session_id}_{uuid.uuid4()}"
        meta = metadata or {}
        meta["session_id"] = session_id

        self.collection.add(
            documents=[text],
            metadatas=[meta],
            ids=[doc_id]
        )

    def retrieve_memory(self, query: str, limit: int = 5) -> list:
        if not self.collection:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        return results.get("documents", [[]])[0]

long_term_memory = LongTermMemory()
