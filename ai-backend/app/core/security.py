"""
Hackathon-appropriate security helpers.

This is intentionally NOT "military grade" - it covers the realistic set of
things a demo/prototype backend should still get right:

- never trust a client-supplied filename
- reject files that are too big or the wrong type
- prevent path traversal when writing/reading uploaded files
- a pluggable auth dependency that is a no-op in demo mode but can be
  switched on with a single static bearer token (good enough for a judged
  hackathon demo; document that JWT/OAuth would replace this in production)
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import Header, HTTPException, status

from app.core.config import get_settings

settings = get_settings()

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9_.-]+")


def safe_filename(original_name: str) -> str:
    """
    Build a filesystem-safe, collision-resistant filename.

    The original name is kept (sanitized) for readability, but a UUID
    prefix guarantees uniqueness and prevents overwrite/path-traversal
    attacks via crafted filenames like `../../etc/passwd`.
    """
    name = Path(original_name or "upload").name  # strips any directory parts
    name = _SAFE_CHARS.sub("_", name).strip("._") or "upload"
    return f"{uuid.uuid4().hex}_{name}"


def validate_upload_extension(filename: str) -> str:
    """Return the lowercase extension if allowed, else raise 400."""
    ext = Path(filename).suffix.lower()
    if ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{ext}'. Allowed types: "
                f"{', '.join(settings.allowed_extensions_list)}"
            ),
        )
    return ext


def validate_upload_size(size_bytes: int) -> None:
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {settings.MAX_UPLOAD_MB}MB upload limit.",
        )


def resolve_within_upload_dir(filename: str) -> Path:
    """
    Resolve `filename` inside the configured upload directory and make sure
    the resolved path does not escape that directory (path traversal guard).
    """
    base = settings.upload_dir_path().resolve()
    candidate = (base / filename).resolve()
    if base not in candidate.parents and candidate != base:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path.")
    return candidate


async def optional_auth(authorization: str | None = Header(default=None)) -> None:
    """
    Lightweight auth dependency.

    - If API_AUTH_ENABLED=false (default, and always true in DEMO_MODE-first
      hackathon setups): this is a no-op, any request is allowed.
    - If API_AUTH_ENABLED=true: a static bearer token (API_STATIC_TOKEN) is
      required. This is a placeholder abstraction - swap it for real
      JWT/OAuth2/session auth before any real deployment.
    """
    if not settings.API_AUTH_ENABLED:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")
    token = authorization.removeprefix("Bearer ").strip()
    if not settings.API_STATIC_TOKEN or token != settings.API_STATIC_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
