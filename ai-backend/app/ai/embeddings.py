"""
Embedding provider abstraction.

`EmbeddingProvider.embed(texts) -> list[list[float]]` is the only contract
the RAG pipeline depends on. Two implementations are provided:

- `SentenceTransformerEmbeddings` — real embeddings using
  `sentence-transformers/all-MiniLM-L6-v2` (configurable via
  EMBEDDING_MODEL). Used whenever the package is installed and can load a
  model (it downloads the model from HuggingFace on first use).
- `HashEmbeddings` — a dependency-free, deterministic fallback so RAG
  still works (retrieval quality is naturally lower, but it is NOT random
  and NOT a network call) when sentence-transformers/torch are not
  installed or there is no internet access, e.g. an offline SIH demo booth.

`get_embedding_provider()` picks the best available option automatically
unless EMBEDDING_PROVIDER forces one explicitly.
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
from abc import ABC, abstractmethod
from typing import List

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

HASH_DIMENSIONS = 256


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        ...

    @property
    @abstractmethod
    def dimensions(self) -> int:
        ...


class SentenceTransformerEmbeddings(EmbeddingProvider):
    def __init__(self, model_name: str | None = None) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name or settings.EMBEDDING_MODEL)
        self._dimensions = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        vectors = self._model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        return [v.tolist() for v in vectors]

    @property
    def dimensions(self) -> int:
        return self._dimensions


class HashEmbeddings(EmbeddingProvider):
    """
    Deterministic bag-of-words hashing embedding.

    Every lowercase word token is hashed into one of `HASH_DIMENSIONS`
    buckets; the resulting vector is L2-normalized. This is a classic
    "hashing trick" feature representation - not as semantically rich as a
    transformer embedding, but fully offline, dependency-free and
    perfectly adequate for a hackathon-scale RAG demo over a handful of
    uploaded documents.
    """

    _word_re = re.compile(r"[a-zA-Z0-9]+")

    def embed(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_one(t) for t in texts]

    def _embed_one(self, text: str) -> List[float]:
        vector = [0.0] * HASH_DIMENSIONS
        for word in self._word_re.findall(text.lower()):
            idx = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16) % HASH_DIMENSIONS
            vector[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    @property
    def dimensions(self) -> int:
        return HASH_DIMENSIONS


def get_embedding_provider() -> EmbeddingProvider:
    mode = settings.EMBEDDING_PROVIDER
    if mode == "hash":
        return HashEmbeddings()
    if mode == "sentence-transformers":
        return SentenceTransformerEmbeddings()
    # auto
    try:
        return SentenceTransformerEmbeddings()
    except Exception as exc:  # noqa: BLE001
        logger.warning("Falling back to HashEmbeddings (offline mode): %s", exc)
        return HashEmbeddings()
