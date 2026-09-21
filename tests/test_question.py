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