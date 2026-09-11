"""
Database setup (SQLAlchemy + SQLite by default).

SQLite is used for the hackathon build because it needs zero setup. The
connection string lives in `.env` (DATABASE_URL) so swapping to Postgres
later is a one-line change, e.g.:

    DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/learning_platform

No application code outside this file needs to change for that swap.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import BASE_DIR, get_settings

settings = get_settings()


def utcnow() -> datetime:
    """
    Current UTC time as a naive datetime.

    Replaces `datetime.utcnow()`, which is deprecated and scheduled for
    removal. The timezone is stripped again on purpose: every timestamp
    column here is a naive `DateTime`, and returning an aware value would
    append a "+00:00" offset to API responses that previously had none.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

_connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}
    # Make sure the sqlite file path resolves relative to ai-backend/
    if settings.DATABASE_URL.startswith("sqlite:///./"):
        rel_path = settings.DATABASE_URL.replace("sqlite:///./", "")
        db_path = BASE_DIR / rel_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    else:
        SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session per-request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Safe to call multiple times."""
    # Import models so they are registered on Base.metadata before create_all.
    from app.models import assessment, competency, employee, material, recommendation  # noqa: F401

    Base.metadata.create_all(bind=engine)
