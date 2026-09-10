"""
Seed / demo data.

Everything in this file is CLEARLY LABELLED demo/mock data (`is_demo_data =
True` on resources, "DEMO Employee" style naming avoided in favour of
realistic-but-fictional profiles). None of it should ever be presented to
end users as real iGOT Karmayogi or NSSTA content - the API layer also
returns a `source: "mock"` flag alongside it (see app/integrations).
"""

from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------
# 1. Employees (>= 3, across different roles, per SIH deliverable spec)
# ---------------------------------------------------------------------
DEMO_EMPLOYEES: List[Dict[str, Any]] = [
    {
        "id": "EMP001",
        "name": "Arun Kumar",
        "designation": "Statistical Officer",
        "department": "National Statistical Office",
        "organization": "Ministry of Statistics & Programme Implementation",
        "email": "arun.kumar@demo.gov.in",
        "location": "New Delhi",
        "experience_years": 6,
        "education": "M.Sc. Statistics",
        "joining_year": 2020,
        "role": "Statistical Officer",
    },
    {
        "id": "EMP002",
        "name": "Priya Sharma",
        "designation": "Data Analyst",
        "department": "Data Informatics & Innovation Division",
        "organization": "Ministry of Statistics & Programme Implementation",
        "email": "priya.sharma@demo.gov.in",
        "location": "New Delhi",
        "experience_years": 3,
        "education": "M.Tech. Data Science",
        "joining_year": 2022,
        "role": "Data Analyst",
    },
    {
        "id": "EMP003",
        "name": "Rahul Verma",
        "designation": "Statistical Programmer",
        "department": "Computer Centre",
        "organization": "Ministry of Statistics & Programme Implementation",
        "email": "rahul.verma@demo.gov.in",
        "location": "Kolkata",
        "experience_years": 4,
        "education": "B.Tech. Computer Science",
        "joining_year": 2021,
        "role": "Statistical Programmer",
    },
]

# ---------------------------------------------------------------------
# 2. Initial competency scores (1-5 scale) per employee/skill.
#    These seed CompetencyScore rows with source="seed"; real scores are
#    produced later by the competency engine from assessment attempts.
# ---------------------------------------------------------------------
DEMO_COMPETENCY_SCORES: Dict[str, List[Dict[str, Any]]] = {
    "EMP001": [
        {"domain": "Statistical", "skill": "Sampling Methodology", "level": 2.8},
        {"domain": "Statistical", "skill": "Survey Design", "level": 3.9},
        {"domain": "Statistical", "skill": "Official Statistics", "level": 4.2},
        {"domain": "Technical", "skill": "Statistical Programming", "level": 2.5},
        {"domain": "Technical", "skill": "Data Visualization", "level": 3.0},
        {"domain": "Digital Governance", "skill": "Data Privacy", "level": 3.2},
        {"domain": "Digital Governance", "skill": "Digital Public Infrastructure", "level": 3.6},
        {"domain": "Behavioural / Managerial", "skill": "Communication", "level": 4.0},
        {"domain": "Behavioural / Managerial", "skill": "Decision Making", "level": 4.0},
    ],
    "EMP002": [
        {"domain": "Statistical", "skill": "Data Quality", "level": 3.4},
        {"domain": "Statistical", "skill": "SDG Indicators", "level": 3.2},
        {"domain": "Technical", "skill": "Python", "level": 4.0},
        {"domain": "Technical", "skill": "SQL", "level": 4.2},
        {"domain": "Technical", "skill": "Data Visualization", "level": 3.8},
        {"domain": "Digital Governance", "skill": "Cybersecurity", "level": 2.9},
        {"domain": "Behavioural / Managerial", "skill": "Project Management", "level": 3.1},
    ],
    "EMP003": [
        {"domain": "Statistical", "skill": "Metadata", "level": 3.0},
        {"domain": "Technical", "skill": "Python", "level": 4.4},
        {"domain": "Technical", "skill": "APIs", "level": 4.0},
        {"domain": "Technical", "skill": "Cloud", "level": 3.5},
        {"domain": "Digital Governance", "skill": "Government Cloud", "level": 3.3},
        {"domain": "Behavioural / Managerial", "skill": "Ethics", "level": 3.4},
    ],
}

# ---------------------------------------------------------------------
# 3. Mock iGOT Karmayogi courses (DEMO DATA - not a live government feed)
# ---------------------------------------------------------------------
DEMO_IGOT_COURSES: List[Dict[str, Any]] = [
    {
        "title": "Statistical Programming with R",
        "category": "Statistical",
        "skill": "Statistical Programming",
        "level": "Intermediate",
        "duration_hours": 8,
        "description": "Learn R programming techniques for statistical analysis, data processing and reproducible workflows.",
        "icon": "💻",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Data Visualization for Statistical Reporting",
        "category": "Technical",
        "skill": "Data Visualization",
        "level": "Intermediate",
        "duration_hours": 4,
        "description": "Develop effective visualizations for communicating statistical findings and official reports.",
        "icon": "📊",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Fundamentals of Official Statistics",
        "category": "Statistical",
        "skill": "Official Statistics",
        "level": "Beginner",
        "duration_hours": 5,
        "description": "Understand the principles, standards and practices behind official statistics.",
        "icon": "📘",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Digital Governance Fundamentals",
        "category": "Digital Governance",
        "skill": "Digital Public Infrastructure",
        "level": "Beginner",
        "duration_hours": 5,
        "description": "Build an understanding of digital governance, public service delivery and data-driven administration.",
        "icon": "🏛️",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Advanced Statistical Methods",
        "category": "Statistical",
        "skill": "Official Statistics",
        "level": "Advanced",
        "duration_hours": 10,
        "description": "Explore advanced statistical methods used in government surveys and analytical studies.",
        "icon": "📈",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Data Management for Public Sector",
        "category": "Technical",
        "skill": "Data Management",
        "level": "Intermediate",
        "duration_hours": 6,
        "description": "Learn practical approaches to managing, validating and organizing public-sector data.",
        "icon": "🗄️",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Python for Data Analysis in Government",
        "category": "Technical",
        "skill": "Python",
        "level": "Intermediate",
        "duration_hours": 8,
        "description": "Apply Python and pandas to clean, analyse and report on administrative and survey data.",
        "icon": "🐍",
        "url": "https://igotkarmayogi.gov.in/",
    },
    {
        "title": "Cybersecurity Essentials for Public Officials",
        "category": "Digital Governance",
        "skill": "Cybersecurity",
        "level": "Beginner",
        "duration_hours": 3,
        "description": "Core cybersecurity hygiene and data-protection practices for government employees.",
        "icon": "🔒",
        "url": "https://igotkarmayogi.gov.in/",
    },
]

# ---------------------------------------------------------------------
# 4. Mock NSSTA TPAC training programs (DEMO DATA)
# ---------------------------------------------------------------------
DEMO_NSSTA_PROGRAMS: List[Dict[str, Any]] = [
    {
        "title": "Sampling Techniques for Official Statistics",
        "category": "Statistical Methodology",
        "provider": "NSSTA TPAC",
        "duration_hours": 6,
        "level": "Intermediate",
        "mode": "Instructor-led",
        "skill": "Sampling Methodology",
    },
    {
        "title": "Advanced Survey Methodology",
        "category": "Statistical Methodology",
        "provider": "NSSTA TPAC",
        "duration_hours": 8,
        "level": "Advanced",
        "mode": "Instructor-led",
        "skill": "Survey Design",
    },
    {
        "title": "Official Statistics: Concepts and Practices",
        "category": "Official Statistics",
        "provider": "NSSTA",
        "duration_hours": 5,
        "level": "Beginner",
        "mode": "Blended",
        "skill": "Official Statistics",
    },
    {
        "title": "Statistical Data Quality Management",
        "category": "Official Statistics",
        "provider": "NSSTA TPAC",
        "duration_hours": 4,
        "level": "Intermediate",
        "mode": "Online",
        "skill": "Data Quality",
    },
    {
        "title": "Data Governance for Public Sector",
        "category": "Data & Technology",
        "provider": "NSSTA",
        "duration_hours": 4,
        "level": "Intermediate",
        "mode": "Online",
        "skill": "Digital Public Infrastructure",
    },
]


def igot_reason(skill: str) -> str:
    return f"Recommended because '{skill}' is a competency area relevant to your current role and skill gaps."


def nssta_reason(skill: str) -> str:
    return f"NSSTA identified '{skill}' as a training focus area based on your competency assessment."


# ---------------------------------------------------------------------
# 5. Generic (non-material) self-assessment quiz generator.
#
# Used by the assessment engine when a learner starts a competency
# self-check WITHOUT an uploaded material (POST /api/assessment/generate
# with no material_id). Every question is a domain-membership check
# derived directly from app/data/competencies.py, so there is zero risk of
# inventing an incorrect statistical/technical fact - the only "fact"
# asserted is "skill X belongs to domain Y", which is true by definition
# of our own catalog.
# ---------------------------------------------------------------------
def generate_generic_quiz(skill: str, domain: str, difficulty: str, num_questions: int) -> List[Dict[str, Any]]:
    from app.data.competencies import COMPETENCY_CATALOG, all_domains

    domains = all_domains()
    other_domains = [d for d in domains if d != domain] or domains
    questions: List[Dict[str, Any]] = []

    templates = [
        (
            f"Which competency domain does the skill '{skill}' primarily belong to?",
            domain,
            other_domains,
        ),
    ]
    # Add a reverse-style question using sibling skills in the same domain, if available.
    siblings = [s for s in COMPETENCY_CATALOG.get(domain, []) if s != skill]
    if siblings:
        pick = siblings[0]
        templates.append(
            (
                f"'{skill}' and '{pick}' are both associated with which competency domain?",
                domain,
                other_domains,
            )
        )

    import random as _random

    idx = 0
    while len(questions) < num_questions:
        question_text, correct_domain, wrong_domains = templates[idx % len(templates)]
        options = [correct_domain] + wrong_domains[:3]
        while len(options) < 4:
            options.append("None of the above")
        options = options[:4]

        rng = _random.Random(f"{skill}-{idx}")
        order = list(range(4))
        rng.shuffle(order)
        shuffled = [options[i] for i in order]
        correct_answer = order.index(0)

        questions.append(
            {
                "question": question_text,
                "options": shuffled,
                "correct_answer": correct_answer,
                "explanation": (
                    f"'{skill}' is catalogued under the '{correct_domain}' competency domain "
                    f"in the platform's competency framework."
                ),
                "competency": skill,
                "difficulty": difficulty,
                "source": "Generic competency self-check (no uploaded material)",
            }
        )
        idx += 1
    return questions[:num_questions]
