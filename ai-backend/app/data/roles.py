"""
Configurable role competency-requirement matrix.

Each role maps to the minimum required level (1-5 scale) per competency
domain. This is seeded into the `roles` / `role_competency_requirements`
tables (see seed.py) so it can be edited later through the database
without touching code - the dict below is simply the initial/default
configuration, not a hardcoded architectural constraint.
"""

from __future__ import annotations

from typing import Dict

ROLE_REQUIREMENTS: Dict[str, Dict[str, float]] = {
    "Statistical Officer": {
        "Statistical": 4.2,
        "Technical": 3.8,
        "Digital Governance": 3.5,
        "Behavioural / Managerial": 4.0,
    },
    "Data Analyst": {
        "Statistical": 3.6,
        "Technical": 4.3,
        "Digital Governance": 3.2,
        "Behavioural / Managerial": 3.4,
    },
    "Statistical Programmer": {
        "Statistical": 3.4,
        "Technical": 4.5,
        "Digital Governance": 3.6,
        "Behavioural / Managerial": 3.0,
    },
}

DEFAULT_ROLE = "Statistical Officer"


def get_role_requirements(role: str) -> Dict[str, float]:
    return ROLE_REQUIREMENTS.get(role, ROLE_REQUIREMENTS[DEFAULT_ROLE])
