"""Tests for QuizManager."""

import pytest
from src.quiz_manager import QuizManager
from src.question import Question


def make_question(qid: int, enabled: bool = True) -> Question:
    """Helper to create a test question."""
    q = Question(
        id=qid,
        type="MCQ",
        topic="Test",
        question=f"Question {qid}?",
        correct_answer="A",
        options=["A", "B", "C", "D"],
    )
    q.enabled = enabled
    return q


def test_add_and_list_questions():
    """Adding a question should store it in the list."""
    qm = QuizManager()
    q = make_question(1)

    qm.add_question(q)

    assert len(qm.list_questions()) == 1
    assert qm.list_questions()[0].id == 1


def test_get_question_by_id():
    """get_question_by_id should find by exact ID."""
    qm = QuizManager()
    qm.add_question(make_question(1))
    qm.add_question(make_question(2))
    qm.add_question(make_question(3))

    assert qm.get_question_by_id(2).id == 2
    assert qm.get_question_by_id(99) is None


def test_enable_and_disable():
    """Enabling/disabling should flip the flag."""
    qm = QuizManager()
    q = make_question(1, enabled=True)
    qm.add_question(q)

    assert qm.disable_question(1) is True
    assert q.enabled is False

    assert qm.enable_question(1) is True
    assert q.enabled is True

    # Non-existent ID
    assert qm.disable_question(99) is False


def test_get_active_questions():
    """Only enabled questions should be returned."""
    qm = QuizManager()
    qm.add_question(make_question(1, enabled=True))
    qm.add_question(make_question(2, enabled=False))
    qm.add_question(make_question(3, enabled=True))

    active = qm.get_active_questions()
    assert len(active) == 2
    assert all(q.enabled for q in active)


def test_get_next_id():
    """get_next_id should return max + 1."""
    qm = QuizManager()
    assert qm.get_next_id() == 1

    qm.add_question(make_question(1))
    assert qm.get_next_id() == 2

    qm.add_question(make_question(5))
    assert qm.get_next_id() == 6


def test_get_weighted_question_empty():
    """Weighted selection on empty collection returns None."""
    qm = QuizManager()
    assert qm.get_weighted_question() is None


def test_get_weighted_question_only_active():
    """Weighted selection should never pick a disabled question."""
    qm = QuizManager()
    qm.add_question(make_question(1, enabled=False))
    qm.add_question(make_question(2, enabled=True))

    for _ in range(20):
        picked = qm.get_weighted_question()
        assert picked is not None
        assert picked.enabled is True
        assert picked.id == 2