"""Chroma-backed vector store for the RAG pipeline.

Embeddings are generated externally by embedding.py (VoyageAI), so the
collection is created *without* an embedding function and vectors are always
passed in explicitly. This keeps indexing and querying on the same model —
letting Chroma fall back to its bundled default model would silently embed
queries with a different model than the documents.

The store persists to a local directory, so chunks only need to be embedded
once. Re-running the script reuses what is already on disk.
"""

import hashlib
from typing import Any, Dict, List, Optional, Sequence

import chromadb

DEFAULT_PERSIST_DIR = "./chroma_db"
DEFAULT_COLLECTION = "report_chunks"


def _chunk_id(content: str) -> str:
    """Stable id derived from content, so re-indexing updates rows instead of duplicating them."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class VectorStore:
    def __init__(
        self,
        collection_name: str = DEFAULT_COLLECTION,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        distance: str = "cosine",
    ):
        if distance not in ("cosine", "l2", "ip"):
            raise ValueError("distance must be 'cosine', 'l2' or 'ip'")

        self.collection_name = collection_name
        self.persist_dir = persist_dir
        self._distance = distance

        # Creates the directory on first use and reopens it on later runs.
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._open_collection()

    def _open_collection(self):
        return self._client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=None,
            metadata={"hnsw:space": self._distance},
        )

    def add(
        self,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Bulk-insert chunks with their pre-computed embeddings. Returns the ids used."""
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Got {len(chunks)} chunks but {len(embeddings)} embeddings."
            )
        if not chunks:
            return []

        ids = ids or [_chunk_id(chunk) for chunk in chunks]

        # upsert (not add) so re-running with the same content is idempotent.
        self._collection.upsert(
            ids=ids,
            documents=list(chunks),
            embeddings=[list(vector) for vector in embeddings],
            metadatas=metadatas,
        )
        return ids

    def search(
        self,
        query_embedding: Sequence[float],
        k: int = 2,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Return the k nearest chunks as dicts with content, metadata and distance."""
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        total = self.count()
        if total == 0:
            return []

        result = self._collection.query(
            query_embeddings=[list(query_embedding)],
            n_results=min(k, total),
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        return [
            {
                "id": chunk_id,
                "content": document,
                "metadata": metadata,
                "distance": distance,
            }
            for chunk_id, document, metadata, distance in zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0],
            )
        ]

    def count(self) -> int:
        return self._collection.count()

    def is_empty(self) -> bool:
        return self.count() == 0

    def reset(self):
        """Drop every stored chunk and start the collection over."""
        self._client.delete_collection(self.collection_name)
        self._collection = self._open_collection()

    def __len__(self) -> int:
        return self.count()

    def __repr__(self) -> str:
        return (
            f"VectorStore(collection='{self.collection_name}', "
            f"count={self.count()}, metric='{self._distance}', "
            f"path='{self.persist_dir}')"
        )
