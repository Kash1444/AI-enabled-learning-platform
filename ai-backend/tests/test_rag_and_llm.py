"""
Tests for the RAG pipeline's Chroma integration and the LLM provider factory.

The Chroma test pins compatibility with chromadb >= 1.0, which embeds
queries through a separate `embed_query()` hook that the 0.5.x-era adapter
did not implement — retrieval failed at runtime while indexing still
appeared to succeed.
"""

import pytest

from app.ai.llm_provider import DemoLLMProvider, get_llm_provider
from app.ai.rag import _EmbeddingFunctionAdapter, get_rag_pipeline
from app.core.config import get_settings


@pytest.fixture()
def rag():
    pipeline = get_rag_pipeline()
    yield pipeline
    pipeline.delete_material("TEST_MATERIAL")


def test_embedding_adapter_implements_chroma_query_hook():
    adapter = _EmbeddingFunctionAdapter.build_from_config({})
    vectors = adapter.embed_query(["sampling methodology"])
    assert len(vectors) == 1
    assert len(vectors[0]) > 0
    # Documents and queries go through the same model here, so the two hooks
    # must agree — otherwise retrieval silently degrades.
    assert adapter.embed_documents(["sampling methodology"]) == vectors


def test_index_then_retrieve_round_trip(rag):
    chunks = [
        {"chunk_id": "TEST_CHUNK_1", "text": "Stratified sampling divides the population into strata."},
        {"chunk_id": "TEST_CHUNK_2", "text": "The design effect measures a loss of precision."},
    ]
    assert rag.index_material("TEST_MATERIAL", chunks) == 2

    hits = rag.retrieve("design effect", material_id="TEST_MATERIAL", top_k=2)
    assert hits, "retrieval returned nothing for an indexed material"
    assert all(h["material_id"] == "TEST_MATERIAL" for h in hits)
    assert {h["chunk_id"] for h in hits} <= {"TEST_CHUNK_1", "TEST_CHUNK_2"}


def test_index_empty_chunk_list_is_a_noop(rag):
    assert rag.index_material("TEST_MATERIAL", []) == 0


def test_demo_mode_always_yields_the_offline_provider():
    settings = get_settings()
    assert settings.DEMO_MODE is True  # forced by tests/conftest.py
    assert isinstance(get_llm_provider(), DemoLLMProvider)


def test_unknown_provider_falls_back_to_demo(monkeypatch):
    """A typo in LLM_PROVIDER must not take the API down mid-demo."""
    import app.ai.llm_provider as llm_module

    monkeypatch.setattr(llm_module.settings, "DEMO_MODE", False)
    monkeypatch.setattr(llm_module.settings, "LLM_PROVIDER", "not-a-real-provider")
    assert isinstance(get_llm_provider(), DemoLLMProvider)


def test_missing_api_key_falls_back_to_demo(monkeypatch):
    import app.ai.llm_provider as llm_module

    monkeypatch.setattr(llm_module.settings, "DEMO_MODE", False)
    monkeypatch.setattr(llm_module.settings, "LLM_PROVIDER", "anthropic")
    monkeypatch.setattr(llm_module.settings, "ANTHROPIC_API_KEY", "")
    assert isinstance(get_llm_provider(), DemoLLMProvider)


def test_anthropic_provider_is_registered():
    """The factory must know the provider even when no key is configured."""
    from app.ai.llm_provider import AnthropicProvider, _PROVIDERS

    assert _PROVIDERS["anthropic"] is AnthropicProvider
