"""
Application configuration.

Everything that can vary between a developer's laptop, a teammate's machine,
or a future production deployment lives here and is read from environment
variables (see `.env.example`). Nothing secret is hardcoded.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # ai-backend/


def _split_csv(value: str) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


class Settings(BaseSettings):
    """Central settings object. Import `get_settings()` to use it."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ---------------------------------------------------------------
    # General
    # ---------------------------------------------------------------
    APP_NAME: str = "AI-enabled Learning Platform - AI Backend"
    ENVIRONMENT: str = "development"
    API_PREFIX: str = "/api"

    # Where `python run.py` binds. Port 8000 is the conventional default, but
    # it is overridable because it is a popular port that other local
    # services (Splunk, Airflow, Django) often already hold.
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # DEMO_MODE=true => the whole platform works with zero external
    # credentials (no OpenAI key, no live iGOT/NSSTA API). This is the
    # safety net for the SIH demo. DEMO_MODE=false switches on the real
    # LLM provider / RAG pipeline whenever the relevant credentials exist.
    DEMO_MODE: bool = True

    # ---------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------
    DATABASE_URL: str = "sqlite:///./storage/app.db"

    # ---------------------------------------------------------------
    # CORS
    # ---------------------------------------------------------------
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return _split_csv(self.CORS_ORIGINS)

    # ---------------------------------------------------------------
    # File storage / uploads
    # ---------------------------------------------------------------
    UPLOAD_DIR: str = "storage/uploads"
    CHROMA_DIR: str = "storage/chroma"
    MAX_UPLOAD_MB: int = 20
    ALLOWED_UPLOAD_EXTENSIONS: str = ".pdf,.docx,.pptx,.txt"

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [e.strip().lower() for e in _split_csv(self.ALLOWED_UPLOAD_EXTENSIONS)]

    # ---------------------------------------------------------------
    # LLM provider
    # ---------------------------------------------------------------
    LLM_PROVIDER: str = "demo"  # demo | anthropic | openai
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-5"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # ---------------------------------------------------------------
    # Embeddings / RAG
    # ---------------------------------------------------------------
    EMBEDDING_PROVIDER: str = "auto"  # auto | sentence-transformers | hash
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_CHUNK_SIZE: int = 900
    RAG_CHUNK_OVERLAP: int = 150
    RAG_TOP_K: int = 4

    # ---------------------------------------------------------------
    # Skill gap thresholds (configurable, see services/skill_gap_engine.py)
    # ---------------------------------------------------------------
    GAP_HIGH_THRESHOLD: float = 1.5
    GAP_MEDIUM_THRESHOLD: float = 0.75

    # ---------------------------------------------------------------
    # Adaptive learning thresholds
    # ---------------------------------------------------------------
    ADAPTIVE_EASY_MAX_PCT: float = 50.0
    ADAPTIVE_INTERMEDIATE_MAX_PCT: float = 75.0
    COMPETENCY_UPDATE_WEIGHT: float = 0.4  # weight given to the *new* evidence

    # ---------------------------------------------------------------
    # iGOT / NSSTA integration (real API placeholders - unused in demo)
    # ---------------------------------------------------------------
    IGOT_API_BASE_URL: str = ""
    IGOT_API_KEY: str = ""
    NSSTA_API_BASE_URL: str = ""
    NSSTA_API_KEY: str = ""

    # ---------------------------------------------------------------
    # Security
    # ---------------------------------------------------------------
    API_AUTH_ENABLED: bool = False
    API_STATIC_TOKEN: str = ""  # used only when API_AUTH_ENABLED=true

    def upload_dir_path(self) -> Path:
        p = BASE_DIR / self.UPLOAD_DIR
        p.mkdir(parents=True, exist_ok=True)
        return p

    def chroma_dir_path(self) -> Path:
        p = BASE_DIR / self.CHROMA_DIR
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache
def get_settings() -> Settings:
    return Settings()
