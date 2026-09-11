"""
RAG (Retrieval-Augmented Generation) pipeline.

Flow implemented here:

    chunks (from document_processor) -> embeddings -> Chroma collection
                                                            |
                                                      retrieve(query)
                                                            |
                                                  relevant chunks (+ scores)

`RAGPipeline` is a thin, swappable wrapper around ChromaDB. Nothing outside
this module (mcq_generator.py, assistant_service.py) talks to Chroma or the
embedding model directly, so either can be replaced independently.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Sequence

from app.ai.embeddings import EmbeddingProvider, get_embedding_provider
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_COLLECTION_NAME = "learning_materials"


class _EmbeddingFunctionAdapter:
    """
    Adapts our EmbeddingProvider to Chroma's EmbeddingFunction protocol.

    The protocol changed between chromadb 0.5.x and 1.x: 0.5.x only ever
    called the object itself, while 1.x embeds *queries* through a separate
    ``embed_query()`` hook (so a model may encode questions and passages
    differently) and asks the function to describe itself via ``name()`` /
    ``get_config()``. We implement the full 1.x surface here and keep
    ``__call__`` as the single source of truth, which leaves the adapter
    working on both major versions.
    """

    def __init__(self, provider: EmbeddingProvider) -> None:
        self._provider = provider

    def __call__(self, input: Sequence[str]) -> List[List[float]]:  # noqa: A002
        return self._provider.embed(list(input))

    # -- chromadb >= 1.0 ------------------------------------------------
    # Our providers embed queries and documents with the same model, so
    # both hooks delegate to __call__ rather than diverging.
    def embed_query(self, input: Sequence[str]) -> List[List[float]]:  # noqa: A002
        return self(input)

    def embed_documents(self, input: Sequence[str]) -> List[List[float]]:  # noqa: A002
        return self(input)

    @staticmethod
    def name() -> str:  # chromadb 1.x calls this unbound; 0.5.x expects a str
        return "custom-embedding-adapter"

    def get_config(self) -> Dict[str, Any]:
        return {}

    @staticmethod
    def build_from_config(config: Dict[str, Any]) -> "_EmbeddingFunctionAdapter":
        return _EmbeddingFunctionAdapter(get_embedding_provider())

    def default_space(self) -> str:
        return "cosine"

    def supported_spaces(self) -> List[str]:
        return ["cosine", "l2", "ip"]

    def is_legacy(self) -> bool:
        return False


class RAGPipeline:
    def __init__(self) -> None:
        import chromadb

        self._embedding_provider = get_embedding_provider()
        self._client = chromadb.PersistentClient(path=str(settings.chroma_dir_path()))
        self._collection = self._client.get_or_create_collection(
            name=_COLLECTION_NAME,
            embedding_function=_EmbeddingFunctionAdapter(self._embedding_provider),
            metadata={"hnsw:space": "cosine"},
        )

    def index_material(self, material_id: str, chunks: List[Dict[str, str]]) -> int:
        """
        Index a material's chunks.

        `chunks` is a list of {"chunk_id": ..., "text": ...} dicts (already
        persisted in SQL by the caller — see api/materials.py). Returns the
        number of chunks indexed.
        """
        if not chunks:
            return 0
        ids = [c["chunk_id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [{"material_id": material_id, "chunk_index": i} for i in range(len(chunks))]
        self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(chunks)

    def retrieve(
        self,
        query: str,
        *,
        material_id: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Return the most relevant chunks for `query`, optionally scoped to
        a single material_id."""
        top_k = top_k or settings.RAG_TOP_K
        where = {"material_id": material_id} if material_id else None
        try:
            count = self._collection.count()
        except Exception:  # noqa: BLE001
            count = 0
        if count == 0:
            return []
        result = self._collection.query(
            query_texts=[query],
            n_results=min(top_k, count),
            where=where,
        )
        hits: List[Dict[str, Any]] = []
        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0] if result.get("distances") else [None] * len(ids)
        for chunk_id, text, meta, distance in zip(ids, documents, metadatas, distances):
            hits.append(
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "material_id": (meta or {}).get("material_id"),
                    "distance": distance,
                }
            )
        return hits

    def delete_material(self, material_id: str) -> None:
        try:
            self._collection.delete(where={"material_id": material_id})
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to delete material %s from Chroma: %s", material_id, exc)


_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """Lazily construct a process-wide singleton (Chroma client is not free
    to open repeatedly)."""
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline
