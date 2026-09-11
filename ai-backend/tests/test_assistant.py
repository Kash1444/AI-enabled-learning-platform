"""
Tests for the AI learning assistant's three routing modes.

In DEMO_MODE there is no language model, so the RAG mode must answer
*extractively* from the retrieved chunks. Previously it forwarded the
prompt to the offline provider, which returned a fixed placeholder — the
retrieval worked but every answer looked broken.
"""

import pytest

from app.services.assistant_service import _extractive_answer


@pytest.fixture()
def material(client, db_session):
    """Upload and index a small material through the real API."""
    from app.models.employee import Employee

    if not db_session.query(Employee).filter(Employee.id == "TEST_EMP_CHAT").first():
        db_session.add(Employee(id="TEST_EMP_CHAT", name="Chat Tester"))
        db_session.commit()

    content = (
        "The design effect measures the ratio of the variance under the actual complex "
        "sample design to the variance under simple random sampling of the same size. "
        "A design effect greater than one indicates a loss of precision. "
        "Stratified sampling divides the population into homogeneous subgroups called strata. "
        "Non-sampling errors include coverage errors, non-response errors and measurement errors."
    )
    response = client.post(
        "/api/materials/upload",
        files={"file": ("designeffect.txt", content, "text/plain")},
        data={
            "title": "Design Effect Notes",
            "competency_domain": "Statistical",
            "competency_skill": "Sampling Methodology",
            "uploaded_by": "trainer",
        },
    )
    assert response.status_code in (200, 201), response.text
    return response.json()["id"]


def test_rag_mode_quotes_the_material_instead_of_a_placeholder(client, material):
    response = client.post(
        "/api/assistant/chat",
        json={
            "employee_id": "TEST_EMP_CHAT",
            "message": "What is the design effect?",
            "material_id": material,
        },
    )
    assert response.status_code == 200
    body = response.json()

    assert body["mode"] == "rag"
    assert body["used_rag"] is True
    assert body["sources"], "a RAG answer must carry citations"
    assert "design effect" in body["answer"].lower()
    assert "templated response" not in body["answer"].lower()


def test_rag_mode_with_unknown_material_is_handled(client):
    response = client.post(
        "/api/assistant/chat",
        json={"employee_id": "TEST_EMP_CHAT", "message": "Anything?", "material_id": "nope"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["used_rag"] is False
    assert "nope" in body["answer"]


def test_profile_mode_answers_from_the_learners_own_data(client, db_session):
    response = client.post(
        "/api/assistant/chat",
        json={"employee_id": "TEST_EMP_CHAT", "message": "What are my biggest skill gaps?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "profile"
    assert body["used_rag"] is False


def test_extractive_answer_prefers_sentences_matching_the_question():
    hits = [
        {
            "chunk_id": "c1",
            "text": (
                "Stratified sampling divides the population into homogeneous subgroups. "
                "A design effect greater than one indicates a loss of precision."
            ),
        }
    ]
    answer = _extractive_answer("What does the design effect indicate?", hits, "Notes")
    assert "design effect greater than one indicates a loss of precision" in answer


def test_extractive_answer_says_so_when_nothing_matches():
    hits = [{"chunk_id": "c1", "text": "Completely unrelated content about payroll processing."}]
    answer = _extractive_answer("zzzz qqqq vvvv", hits, "Notes")
    assert "nothing that directly answers" in answer.lower()
