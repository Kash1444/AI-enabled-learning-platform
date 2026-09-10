"""
Seed the database with demo data: roles, role requirements, employees,
initial competency scores, and an initial skill-gap snapshot.

Usage (from inside ai-backend/, with the virtual environment active):

    python seed.py

Safe to re-run: existing rows are left alone (it exits early if employees
already exist), so it won't duplicate data on a second run.
"""

from __future__ import annotations

import logging

from app.core.database import SessionLocal, init_db
from app.data.demo_data import DEMO_COMPETENCY_SCORES, DEMO_EMPLOYEES
from app.data.roles import ROLE_REQUIREMENTS
from app.models.competency import CompetencyScore
from app.models.employee import Employee, Role, RoleCompetencyRequirement
from app.services.skill_gap_engine import compute_skill_gaps, persist_skill_gaps

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("seed")


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Employee).count() > 0:
            logger.info("Employees already exist - skipping seed (delete storage/app.db to reseed).")
            return

        logger.info("Seeding roles and competency requirements...")
        role_objs: dict[str, Role] = {}
        for role_name, domain_requirements in ROLE_REQUIREMENTS.items():
            role = Role(name=role_name, description=f"{role_name} role in India's Official Statistical System")
            db.add(role)
            db.flush()  # get role.id
            for domain, level in domain_requirements.items():
                db.add(RoleCompetencyRequirement(role_id=role.id, domain=domain, required_level=level))
            role_objs[role_name] = role
        db.commit()

        logger.info("Seeding %d demo employees...", len(DEMO_EMPLOYEES))
        for emp in DEMO_EMPLOYEES:
            role = role_objs.get(emp["role"])
            db.add(
                Employee(
                    id=emp["id"],
                    name=emp["name"],
                    designation=emp["designation"],
                    department=emp["department"],
                    organization=emp["organization"],
                    email=emp["email"],
                    location=emp["location"],
                    experience_years=emp["experience_years"],
                    education=emp["education"],
                    joining_year=emp["joining_year"],
                    role_id=role.id if role else None,
                )
            )
        db.commit()

        logger.info("Seeding initial competency scores...")
        for employee_id, scores in DEMO_COMPETENCY_SCORES.items():
            for s in scores:
                db.add(
                    CompetencyScore(
                        employee_id=employee_id,
                        domain=s["domain"],
                        skill=s["skill"],
                        level=s["level"],
                        source="seed",
                    )
                )
        db.commit()

        logger.info("Computing initial skill-gap snapshots...")
        for employee in db.query(Employee).all():
            gaps = compute_skill_gaps(db, employee)
            persist_skill_gaps(db, employee.id, gaps)

        logger.info("Seed complete. %d employees ready.", len(DEMO_EMPLOYEES))
    finally:
        db.close()


if __name__ == "__main__":
    seed()
