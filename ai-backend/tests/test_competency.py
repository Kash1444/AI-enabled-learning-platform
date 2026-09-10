from app.schemas.competency import AnswerInput
from app.services.competency_engine import score_answers_for_skill, score_assessment


def _answer(is_correct: bool, difficulty: str = "Intermediate", weight: float = 1.0) -> AnswerInput:
    return AnswerInput(
        question_id="q1",
        skill="Python",
        domain="Technical",
        difficulty=difficulty,
        is_correct=is_correct,
        weight=weight,
    )


def test_all_correct_gives_max_level():
    level, _ = score_answers_for_skill([_answer(True), _answer(True), _answer(True)])
    assert level == 5.0


def test_all_incorrect_gives_min_level():
    level, _ = score_answers_for_skill([_answer(False), _answer(False)])
    assert level == 1.0


def test_deterministic_and_reproducible():
    answers = [_answer(True), _answer(False), _answer(True), _answer(False)]
    level_a, _ = score_answers_for_skill(answers)
    level_b, _ = score_answers_for_skill(answers)
    assert level_a == level_b
    assert 1.0 <= level_a <= 5.0


def test_harder_correct_questions_score_higher_than_easier_ones():
    easy_correct = [_answer(True, difficulty="Easy"), _answer(False, difficulty="Easy")]
    advanced_correct = [_answer(True, difficulty="Advanced"), _answer(False, difficulty="Easy")]
    level_easy, _ = score_answers_for_skill(easy_correct)
    level_advanced, _ = score_answers_for_skill(advanced_correct)
    assert level_advanced > level_easy


def test_score_assessment_groups_by_skill():
    answers = [
        AnswerInput(question_id="1", skill="Python", domain="Technical", is_correct=True),
        AnswerInput(question_id="2", skill="Sampling Methodology", domain="Statistical", is_correct=False),
    ]
    result = score_assessment(answers)
    assert set(result.keys()) == {"Python", "Sampling Methodology"}
    assert result["Python"]["level"] > result["Sampling Methodology"]["level"]


def test_assess_endpoint_persists_and_returns_domain_scores(client, db_session):
    from app.models.employee import Employee

    db_session.add(Employee(id="TEST_EMP_1", name="Test User"))
    db_session.commit()

    payload = {
        "employee_id": "TEST_EMP_1",
        "answers": [
            {
                "question_id": "q1",
                "skill": "Python",
                "domain": "Technical",
                "difficulty": "Intermediate",
                "is_correct": True,
                "weight": 1.0,
            },
            {
                "question_id": "q2",
                "skill": "Python",
                "domain": "Technical",
                "difficulty": "Intermediate",
                "is_correct": True,
                "weight": 1.0,
            },
        ],
    }
    response = client.post("/api/competency/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == "TEST_EMP_1"
    assert data["skill_levels"]["Python"] == 5.0
    assert any(d["domain"] == "Technical" for d in data["domain_scores"])
