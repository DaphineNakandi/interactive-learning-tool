"""Tests for storage module."""

from src.storage import (
    load_questions,
    save_questions,
    save_result,
    load_results,
)
from src.question import Question


def make_question(qid: int) -> Question:
    return Question(
        id=qid,
        type="MCQ",
        topic="Test",
        question=f"Question {qid}?",
        correct_answer="A",
        options=["A", "B", "C", "D"],
    )


def test_save_and_load_round_trip(tmp_path):
    """Save questions, load them back, verify all fields survive."""
    filepath = str(tmp_path / "questions.json")
    original = [make_question(1), make_question(2)]
    original[0].times_shown = 5
    original[0].times_correct = 3
    original[0].enabled = False

    save_questions(original, filepath)
    loaded = load_questions(filepath)

    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].times_shown == 5
    assert loaded[0].times_correct == 3
    assert loaded[0].enabled is False
    assert loaded[1].id == 2
    assert loaded[1].enabled is True


def test_load_missing_file_returns_empty():
    """Loading a non-existent file returns an empty list."""
    result = load_questions("does_not_exist.json")
    assert result == []


def test_save_result_appends(tmp_path):
    """save_result should append, not overwrite."""
    filepath = str(tmp_path / "results.txt")
    save_result(7, 10, filepath)
    save_result(9, 10, filepath)

    results = load_results(filepath)
    assert len(results) == 2
    assert "7/10" in results[0]
    assert "9/10" in results[1]


def test_load_results_missing_file():
    """Loading a missing results file returns an empty list."""
    assert load_results("does_not_exist.txt") == []