"""
Extensible competency catalog.

This is DATA, not architecture: nothing in app/services or app/models
assumes these exact domains/skills exist. Add or edit entries here (or load
them from a DB/admin UI later) and the rest of the system keeps working.

Domains follow the SIH problem statement (26101):
  - Statistical
  - Technical
  - Digital Governance
  - Behavioural / Managerial
"""

from __future__ import annotations

from typing import Dict, List

COMPETENCY_CATALOG: Dict[str, List[str]] = {
    "Statistical": [
        "Survey Design",
        "Sampling Methodology",
        "National Accounts",
        "Price Statistics",
        "Labour Statistics",
        "Agricultural Statistics",
        "Industrial Statistics",
        "SDG Indicators",
        "Metadata",
        "Data Quality",
        "Statistical Programming",
        "Official Statistics",
    ],
    "Technical": [
        "Python",
        "R",
        "SQL",
        "Stata",
        "SPSS",
        "SAS",
        "GIS",
        "Data Visualization",
        "AI/ML",
        "Cloud",
        "APIs",
        "Open Data",
        "Data Management",
    ],
    "Digital Governance": [
        "Cybersecurity",
        "Data Privacy",
        "Digital Signatures",
        "Government Cloud",
        "Digital Public Infrastructure",
    ],
    "Behavioural / Managerial": [
        "Leadership",
        "Communication",
        "Project Management",
        "Ethics",
        "Decision Making",
        "Change Management",
    ],
}


def all_domains() -> List[str]:
    return list(COMPETENCY_CATALOG.keys())


def skills_in_domain(domain: str) -> List[str]:
    return COMPETENCY_CATALOG.get(domain, [])


def domain_for_skill(skill: str) -> str:
    """Look up which domain a skill belongs to. Falls back to 'Technical'
    for unrecognised skills so the pipeline never breaks on new/custom
    skills entered by a trainer."""
    for domain, skills in COMPETENCY_CATALOG.items():
        if skill in skills:
            return domain
    return "Technical"
