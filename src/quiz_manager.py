from src.question import Question

class QuizManager:
    """Manages the collection of questions."""

    def __init__(self) -> None:
        self.questions: list[Question] = []

    def add_question(self, question: Question) -> None:
        """Add a question to the collection."""
        self.questions.append(question)

    def get_question_by_id(self, question_id: int) -> Question | None:
        """Find and return a question by its ID."""
        for question in self.questions:
            if question.id == question_id:
                return question

        return None

    def enable_question(self, question_id: int) -> bool:
        """Enable a question by its ID."""
        question = self.get_question_by_id(question_id)

        if question is None:
            return False

        question.enabled = True
        return True

    def disable_question(self, question_id: int) -> bool:
        """Disable a question by its ID."""
        question = self.get_question_by_id(question_id)

        if question is None:
            return False

        question.enabled = False
        return True

    def list_questions(self) -> list[Question]:
        """Return all questions in the collection."""
        return self.questions
        

    def get_active_questions(self) -> list[Question]:
        """Return all enabled questions in the collection."""
        return [question for question in self.questions if question.enabled]


    def get_next_id(self) -> int:
        """
        Return the next avaiable question ID.

        Returns:
            THe next integer ID (max existing + 1, or 1 if empty).
        """

        if not self.questions:
            return 1
        return max(q.id for q in self.questions) + 1