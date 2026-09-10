"""
Shared pytest fixtures.

Tests must run without any LLM API key. We force DEMO_MODE=true and a
dependency-free hash embedding provider, and point the database + storage
directories at a temporary location so tests never touch developer data.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Ensure `app` is importable when pytest is run from ai-backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TEST_DIR = Path(__file__).resolve().parent
TMP_STORAGE = TEST_DIR / "_tmp_storage"
TMP_STORAGE.mkdir(exist_ok=True)

os.environ["DEMO_MODE"] = "true"
os.environ["DATABASE_URL"] = f"sqlite:///{(TMP_STORAGE / 'test.db').as_posix()}"
os.environ["EMBEDDING_PROVIDER"] = "hash"
os.environ["UPLOAD_DIR"] = str((TMP_STORAGE / "uploads").relative_to(Path(__file__).resolve().parent.parent))
os.environ["CHROMA_DIR"] = str((TMP_STORAGE / "chroma").relative_to(Path(__file__).resolve().parent.parent))
os.environ["CORS_ORIGINS"] = "http://localhost:5173"

from app.core.database import Base, engine, init_db  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _setup_database():
    # Fresh schema for the whole test session.
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db_session():
    from app.core.database import SessionLocal

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
