"""
FastAPI application entrypoint.

Run with:

    uvicorn app.main:app --reload

See README.md for full setup instructions (Windows PowerShell included).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import assessments, assistant, competency, materials, recommendations
from app.core.config import get_settings
from app.core.database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables before the first request is served."""
    init_db()
    logger.info(
        "Database initialized. DEMO_MODE=%s, LLM_PROVIDER=%s",
        settings.DEMO_MODE,
        settings.LLM_PROVIDER,
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    description=(
        "AI layer for the AI-enabled Learning Platform (SIH 2026, Problem Statement 26101). "
        "Provides competency assessment, skill-gap analysis, personalized recommendations "
        "(iGOT Karmayogi / NSSTA TPAC), RAG-grounded MCQ generation from trainer-uploaded "
        "materials, quiz evaluation with adaptive learning, and an AI learning assistant. "
        f"DEMO_MODE is currently **{settings.DEMO_MODE}**."
    ),
    version="1.0.0",
    contact={"name": "AI-enabled Learning Platform Team"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------
# Global exception handlers: never leak stack traces to API clients.
# ---------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.info("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error.", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred."},
    )


@app.get("/api/health", tags=["Health"], summary="Health check")
def health() -> dict:
    """Lightweight health check - also reports DEMO_MODE so the frontend/demo
    operator can confirm the backend is running in the expected mode."""
    return {
        "status": "ok",
        "demo_mode": settings.DEMO_MODE,
        "llm_provider": settings.LLM_PROVIDER if not settings.DEMO_MODE else "demo",
        "app": settings.APP_NAME,
    }


app.include_router(competency.router)
app.include_router(recommendations.router)
app.include_router(materials.router)
app.include_router(assessments.router)
app.include_router(assistant.router)
