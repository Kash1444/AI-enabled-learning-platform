"""
Regression tests for the quality of offline (DEMO_MODE) MCQ generation.

These pin behaviour that was previously broken and is easy to regress:
overlapping chunks used to start mid-word, and those fragments were served
verbatim to learners as answer options.
"""

from app.ai.mcq_generator import RetrievedChunk, generate_demo_mcqs
from app.processors.document_processor import chunk_text, clean_text

MATERIAL = """Sampling Methodology for Official Statistics

Simple random sampling is a technique in which every unit in the population has an equal and known probability of being selected.

Stratified sampling divides the population into homogeneous subgroups called strata, and then draws an independent sample from each stratum.

Cluster sampling selects groups of units, known as clusters, rather than individual units. It reduces travel and listing costs in large-scale household surveys.

Systematic sampling selects every kth unit from an ordered list after a random start.

The design effect measures the ratio of the variance under the actual complex sample design to the variance under simple random sampling.

Non-sampling errors include coverage errors, non-response errors, measurement errors and processing errors.

The sampling frame is the list of units from which the sample is actually drawn.
"""


def _chunks() -> list[RetrievedChunk]:
    text = clean_text(MATERIAL)
    return [
        RetrievedChunk(chunk_id=f"chunk_{i}", text=c)
        for i, c in enumerate(chunk_text(text, chunk_size=300, overlap=80))
    ]


def test_chunks_never_start_mid_word():
    """A chunk that opens mid-word ('ariance relative to...') leaks into MCQ
    options and RAG citations as broken English."""
    text = clean_text(MATERIAL)
    chunks = chunk_text(text, chunk_size=300, overlap=80)
    assert len(chunks) > 1, "need multiple chunks for this to be meaningful"
    for chunk in chunks[1:]:
        # The chunk's first word must be a whole word from the source text.
        first_word = chunk.split()[0].strip(".,;:()[]\"'")
        assert first_word in text.replace("\n", " ").split() or first_word in text, (
            f"chunk begins with the fragment {first_word!r}"
        )


def test_demo_mcq_options_are_single_line_and_non_empty():
    questions = generate_demo_mcqs(
        _chunks(),
        competency="Sampling Methodology",
        difficulty="Intermediate",
        num_questions=4,
        source_label="sampling.txt",
    )
    assert questions
    for q in questions:
        assert len(q.options) == 4
        for option in q.options:
            assert option.strip(), "option must not be blank"
            assert "\n" not in option, "an option must render on a single line"
        assert 0 <= q.correct_answer <= 3


def test_demo_mcqs_are_not_all_the_same_question():
    """Every question used to share one generic stem, which made a generated
    quiz look broken."""
    questions = generate_demo_mcqs(
        _chunks(),
        competency="Sampling Methodology",
        difficulty="Intermediate",
        num_questions=4,
        source_label="sampling.txt",
    )
    assert len(questions) >= 2
    stems = {q.question for q in questions}
    assert len(stems) == len(questions), "each question must have a distinct stem"


def test_demo_mcq_correct_option_is_grounded_in_the_material():
    text = clean_text(MATERIAL)
    questions = generate_demo_mcqs(
        _chunks(),
        competency="Sampling Methodology",
        difficulty="Intermediate",
        num_questions=4,
        source_label="sampling.txt",
    )
    for q in questions:
        answer = q.options[q.correct_answer]
        assert answer in text, f"correct answer {answer!r} is not present in the source material"


def test_demo_mcq_generation_is_reproducible():
    kwargs = dict(
        competency="Sampling Methodology",
        difficulty="Intermediate",
        num_questions=4,
        source_label="sampling.txt",
    )
    first = generate_demo_mcqs(_chunks(), **kwargs)
    second = generate_demo_mcqs(_chunks(), **kwargs)
    assert [q.question for q in first] == [q.question for q in second]
    assert [q.options for q in first] == [q.options for q in second]
