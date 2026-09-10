import pytest
from pydantic import ValidationError

from app.ai.mcq_generator import GeneratedMCQ


def test_generated_mcq_rejects_bad_correct_answer_index():
    with pytest.raises(ValidationError):
        GeneratedMCQ(
            question="Q?",
            options=["a", "b", "c", "d"],
            correct_answer=7,
            explanation="because",
        )


def test_generated_mcq_rejects_duplicate_options():
    with pytest.raises(ValidationError):
        GeneratedMCQ(
            question="Q?",
            options=["a", "a", "c", "d"],
            correct_answer=0,
            explanation="because",
        )


def test_generated_mcq_rejects_wrong_option_count():
    with pytest.raises(ValidationError):
        GeneratedMCQ(question="Q?", options=["a", "b", "c"], correct_answer=0, explanation="because")


def test_generic_quiz_generation_is_grounded_in_catalog():
    from app.data.demo_data import generate_generic_quiz

    questions = generate_generic_quiz("Python", "Technical", "Easy", 3)
    assert len(questions) == 3
    for q in questions:
        assert len(q["options"]) == 4
        assert 0 <= q["correct_answer"] <= 3
        assert q["options"][q["correct_answer"]] == "Technical"


def test_generate_and_evaluate_assessment_end_to_end(client, db_session):
    from app.models.employee import Employee

    db_session.add(Employee(id="TEST_EMP_4", name="Assess Tester"))
    db_session.commit()

    gen_payload = {
        "competency": "Python",
        "domain": "Technical",
        "num_questions": 3,
        "difficulty": "Easy",
        "employee_id": "TEST_EMP_4",
    }
    gen_resp = client.post("/api/assessment/generate", json=gen_payload)
    assert gen_resp.status_code == 201
    assessment = gen_resp.json()
    assert assessment["generated_by"] == "demo"
    assert len(assessment["questions"]) == 3

    # Learner-facing GET should not leak the answer key.
    get_resp = client.get(f"/api/assessment/{assessment['id']}")
    assert get_resp.status_code == 200
    learner_view = get_resp.json()
    assert "correct_answer" not in learner_view["questions"][0]

    # Answer everything correctly using the answer key we DO have from generation.
    answers = {q["id"]: q["correct_answer"] for q in assessment["questions"]}
    eval_payload = {
        "assessment_id": assessment["id"],
        "employee_id": "TEST_EMP_4",
        "answers": answers,
    }
    eval_resp = client.post("/api/assessment/evaluate", json=eval_payload)
    assert eval_resp.status_code == 200
    result = eval_resp.json()
    assert result["score"] == 3
    assert result["percentage"] == 100.0
    assert result["next_recommended_difficulty"] == "Advanced"
    assert result["competency_impact"][0]["after"] > result["competency_impact"][0]["before"]


def test_evaluate_missing_assessment_returns_404(client):
    response = client.post(
        "/api/assessment/evaluate",
        json={"assessment_id": "does_not_exist", "employee_id": "TEST_EMP_4", "answers": {"q1": 0}},
    )
    assert response.status_code == 404
