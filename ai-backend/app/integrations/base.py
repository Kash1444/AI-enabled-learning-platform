"""
Abstract provider interface shared by iGOT and NSSTA integrations.

Design intent
-------------
Neither iGOT Karmayogi nor NSSTA TPAC expose public credentials for this
hackathon, so we cannot (and must not pretend to) call a live government
API. Instead we define the *shape* of that integration precisely, so that
swapping in real credentials later is a matter of implementing one class -
nothing in the services layer needs to change.

    provider = get_igot_provider()          # returns Mock or Real
    courses = provider.search_courses(...)  # same call either way
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class CourseProviderInterface(ABC):
    """Interface implemented by any course-catalog integration (iGOT-like)."""

    @abstractmethod
    def search_courses(
        self,
        *,
        category: Optional[str] = None,
        skill: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return a list of course dicts matching the given filters."""

    @abstractmethod
    def get_course(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Return a single course dict, or None if not found."""


class ProgramProviderInterface(ABC):
    """Interface implemented by any training-program integration (NSSTA-like)."""

    @abstractmethod
    def search_programs(
        self,
        *,
        category: Optional[str] = None,
        skill: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return a list of program dicts matching the given filters."""

    @abstractmethod
    def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        """Return a single program dict, or None if not found."""
