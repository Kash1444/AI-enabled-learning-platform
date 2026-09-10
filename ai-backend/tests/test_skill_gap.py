from app.services.skill_gap_engine import classify_priority, compute_skill_gaps


def test_priority_thresholds():
    assert classify_priority(2.0) == "High"
    assert classify_priority(1.5) == "High"
    assert classify_priority(1.0) == "Medium"
    assert classify_priority(0.75) == "Medium"
    assert classify_priority(0.5) == "Low"
    assert classify_priority(0.0) == "Low"


def test_compute_skill_gaps_for_seeded_employee(client, db_session):
    """Uses the DB directly to set up a minimal employee + role + score,
    then verifies gap = required - current and priority classification."""
    from app.models.competency import CompetencyScore
    from app.models.employee import Employee, Role, RoleCompetencyRequirement

    role = Role(name="Test Role")
    db_session.add(role)
    db_session.flush()
    db_session.add(RoleCompetencyRequirement(role_id=role.id, domain="Technical", required_level=4.0))
    db_session.commit()

    employee = Employee(id="TEST_EMP_2", name="Gap Tester", role_id=role.id)
    db_session.add(employee)
    db_session.add(
        CompetencyScore(employee_id="TEST_EMP_2", domain="Technical", skill="Python", level=2.0, source="seed")
    )
    db_session.commit()
    db_session.refresh(employee)

    gaps = compute_skill_gaps(db_session, employee)
    assert len(gaps) == 1
    gap = gaps[0]
    assert gap.skill == "Python"
    assert gap.current == 2.0
    assert gap.required == 4.0
    assert gap.gap == 2.0
    assert gap.priority == "High"
    assert "Python" in gap.description
    assert gap.recommended_action


def test_no_gap_when_current_meets_required(client, db_session):
    from app.models.competency import CompetencyScore
    from app.models.employee import Employee, Role, RoleCompetencyRequirement

    role = Role(name="Test Role 2")
    db_session.add(role)
    db_session.flush()
    db_session.add(RoleCompetencyRequirement(role_id=role.id, domain="Technical", required_level=3.0))
    db_session.commit()

    employee = Employee(id="TEST_EMP_3", name="No Gap", role_id=role.id)
    db_session.add(employee)
    db_session.add(
        CompetencyScore(employee_id="TEST_EMP_3", domain="Technical", skill="SQL", level=4.5, source="seed")
    )
    db_session.commit()
    db_session.refresh(employee)

    gaps = compute_skill_gaps(db_session, employee)
    assert gaps == []
