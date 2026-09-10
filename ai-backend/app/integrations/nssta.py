"""
NSSTA TPAC training-program integration.

Mirrors app/integrations/igot.py: a mock provider serving clearly-labelled
demo data, and a documented placeholder for the real NSSTA integration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.data.demo_data import DEMO_NSSTA_PROGRAMS, nssta_reason
from app.integrations.base import ProgramProviderInterface

settings = get_settings()


class MockNSSTAProvider(ProgramProviderInterface):
    """Serves demo NSSTA TPAC-style programs. Clearly not a live feed."""

    def __init__(self) -> None:
        self._programs: List[Dict[str, Any]] = []
        for i, program in enumerate(DEMO_NSSTA_PROGRAMS, start=1):
            item = dict(program)
            item["id"] = f"nssta_demo_{i:03d}"
            item["is_demo_data"] = True
            item["reason"] = nssta_reason(program["skill"])
            self._programs.append(item)

    def search_programs(
        self,
        *,
        category: Optional[str] = None,
        skill: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        results = self._programs
        if category and category != "All":
            results = [p for p in results if p["category"] == category]
        if skill:
            results = [p for p in results if p["skill"].lower() == skill.lower()]
        if query:
            q = query.lower()
            results = [p for p in results if q in p["title"].lower() or q in p["skill"].lower()]
        return results[:limit]

    def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        return next((p for p in self._programs if p["id"] == program_id), None)


class RealNSSTAProvider(ProgramProviderInterface):
    """
    Placeholder for the real NSSTA TPAC API integration.

    To implement: use `settings.NSSTA_API_BASE_URL` / `settings.NSSTA_API_KEY`
    and map responses onto the same dict shape as MockNSSTAProvider.
    """

    def __init__(self) -> None:
        if not settings.NSSTA_API_BASE_URL or not settings.NSSTA_API_KEY:
            raise RuntimeError(
                "RealNSSTAProvider requires NSSTA_API_BASE_URL and NSSTA_API_KEY to be set in .env"
            )

    def search_programs(self, **kwargs: Any) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "Real NSSTA TPAC API integration is not available in this build. "
            "Configure NSSTA_API_BASE_URL/NSSTA_API_KEY and implement this method."
        )

    def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("See search_programs() docstring.")


def get_nssta_provider() -> ProgramProviderInterface:
    if settings.NSSTA_API_BASE_URL and settings.NSSTA_API_KEY:
        try:
            return RealNSSTAProvider()
        except Exception:
            return MockNSSTAProvider()
    return MockNSSTAProvider()
