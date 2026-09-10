"""
iGOT Karmayogi course-catalog integration.

- `MockIGOTProvider` — always available, serves clearly-labelled demo data
  from app/data/demo_data.py. Used whenever IGOT_API_BASE_URL/IGOT_API_KEY
  are not configured (i.e. always, in the current hackathon build).
- `RealIGOTProvider` — a documented placeholder for the future live
  integration. It intentionally raises NotImplementedError with guidance
  rather than silently returning fake data pretending to be real.

Call `get_igot_provider()` everywhere instead of instantiating a provider
directly, so switching providers is a one-line config change.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.data.demo_data import DEMO_IGOT_COURSES, igot_reason
from app.integrations.base import CourseProviderInterface

settings = get_settings()


class MockIGOTProvider(CourseProviderInterface):
    """Serves demo iGOT-style courses. Clearly not a live government feed."""

    def __init__(self) -> None:
        # Stable, deterministic IDs so repeated calls / tests are reproducible.
        self._courses: List[Dict[str, Any]] = []
        for i, course in enumerate(DEMO_IGOT_COURSES, start=1):
            item = dict(course)
            item["id"] = f"igot_demo_{i:03d}"
            item["provider"] = "iGOT Karmayogi"
            item["is_demo_data"] = True
            item["reason"] = igot_reason(course["skill"])
            self._courses.append(item)

    def search_courses(
        self,
        *,
        category: Optional[str] = None,
        skill: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        results = self._courses
        if category and category != "All":
            results = [c for c in results if c["category"] == category]
        if skill:
            results = [c for c in results if c["skill"].lower() == skill.lower()]
        if query:
            q = query.lower()
            results = [
                c
                for c in results
                if q in c["title"].lower() or q in c["skill"].lower() or q in c["description"].lower()
            ]
        return results[:limit]

    def get_course(self, course_id: str) -> Optional[Dict[str, Any]]:
        return next((c for c in self._courses if c["id"] == course_id), None)


class RealIGOTProvider(CourseProviderInterface):
    """
    Placeholder for the real iGOT Karmayogi API integration.

    To implement: use `settings.IGOT_API_BASE_URL` / `settings.IGOT_API_KEY`
    (populated from `.env`) to call the official iGOT API, map its response
    fields onto the same dict shape produced by MockIGOTProvider (id, title,
    category, skill, level, duration_hours, description, icon, provider,
    url, is_demo_data=False, reason), and return that instead.
    """

    def __init__(self) -> None:
        if not settings.IGOT_API_BASE_URL or not settings.IGOT_API_KEY:
            raise RuntimeError(
                "RealIGOTProvider requires IGOT_API_BASE_URL and IGOT_API_KEY to be set in .env"
            )

    def search_courses(self, **kwargs: Any) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "Real iGOT Karmayogi API integration is not available in this build. "
            "Configure IGOT_API_BASE_URL/IGOT_API_KEY and implement this method "
            "against the official iGOT API contract."
        )

    def get_course(self, course_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("See search_courses() docstring.")


def get_igot_provider() -> CourseProviderInterface:
    """Factory: returns the real provider if fully configured, else the mock."""
    if settings.IGOT_API_BASE_URL and settings.IGOT_API_KEY:
        try:
            return RealIGOTProvider()
        except Exception:
            return MockIGOTProvider()
    return MockIGOTProvider()
