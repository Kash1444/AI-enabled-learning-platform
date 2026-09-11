"""
Start the API server.

    python run.py

Equivalent to `uvicorn app.main:app --reload`, but it reads HOST/PORT from
.env so the port only has to be configured in one place (it has to match
VITE_API_URL in frontend/.env).
"""

from __future__ import annotations

import uvicorn

from app.core.config import get_settings


def main() -> None:
    settings = get_settings()
    print(f"Starting {settings.APP_NAME}")
    print(f"  API      http://{settings.HOST}:{settings.PORT}{settings.API_PREFIX}")
    print(f"  Docs     http://{settings.HOST}:{settings.PORT}/docs")
    print(f"  DEMO_MODE={settings.DEMO_MODE}  LLM_PROVIDER={settings.LLM_PROVIDER}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    )


if __name__ == "__main__":
    main()
