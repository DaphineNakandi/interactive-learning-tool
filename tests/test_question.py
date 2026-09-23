from src.question import Question
from src.quiz_manager import QuizManager


def test_question_creation():
    """Test that a Question is created with correct attributes."""
    question = Question(
        id=1,
        type="MCQ",
        topic="Python",
        question="What's a list?",
        options=["A collection of items", "A function", "A loop", "A database"],
        correct_answer="A collection of items",
    )

    assert question.id == 1
    assert question.type == "MCQ"
    assert question.topic == "Python"
    assert question.question == "What's a list?"
    assert question.correct_answer == "A collection of items"
    assert question.options == ["A collection of items", "A function", "A loop", "A database"]
    assert question.enabled is True
    assert question.times_shown == 0
    assert question.times_correct == 0
    assert question.times_incorrect == 0


def test_evaluate_mcq_wrong_option():
    """Regression test: a wrong option should NOT be marked correct."""
    q = Question(
        id=1, type="MCQ", topic="Python",
        question="What is a list?",
        options=["A collection of items", "A function", "A loop", "A database"],
        correct_answer="A",
    )

    # Correct answers
    assert q.evaluate_mcq("A") is True
    assert q.evaluate_mcq("A collection of items") is True
    assert q.evaluate_mcq("a") is True
    assert q.evaluate_mcq("a collection of items") is True

    # Wrong answers (regression — these used to return True!)
    assert q.evaluate_mcq("A function") is False
    assert q.evaluate_mcq("B") is False
    assert q.evaluate_mcq("A loop") is False
    assert q.evaluate_mcq("A database") is False


def test_get_weight_unseen():
    """Unseen questions should get weight 0.5."""
    q = Question(id=1, type="MCQ", topic="T", question="Q?", correct_answer="A")
    assert q.get_weight() == 0.5


def test_get_weight_performance():
    """Lower correct percentage should give higher weight."""
    q = Question(id=1, type="MCQ", topic="T", question="Q?", correct_answer="A")

    # 0% correct (never right) → highest weight
    q.times_shown = 10
    q.times_correct = 0
    weight_low = q.get_weight()

    # 100% correct → lowest weight
    q.times_correct = 10
    weight_high = q.get_weight()

    assert weight_low > weight_high