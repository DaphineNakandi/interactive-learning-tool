"""User interface for the AI Learning Companion."""

from src.quiz_manager import QuizManager
from src.llm_client import LLMClient
from src.question import Question
from src.storage import load_questions, save_questions


QUESTIONS_FILE = "data/questions.json"


class App:
    """The main CLI application."""

    def __init__(self) -> None:
        """Initialize the app and load questions from disk."""
        self.quiz_manager = QuizManager()
        self.llm_client = LLMClient()
        self.quiz_manager.questions = load_questions(QUESTIONS_FILE)

    def run(self) -> None:
        """Run the main menu loop."""
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "6":
                print("Goodbye!")
                break
            elif choice == "1":
                self.generate_questions_mode()
            elif choice == "2":
                self.statistics_mode()
            elif choice == "3":
                print("[Practice Mode — not yet implemented]")
            elif choice == "4":
                print("[Test Mode — not yet implemented]")
            elif choice == "5":
                print("[Manage Questions — not yet implemented]")
            else:
                print("Invalid choice. Please enter 1-6.")

    def show_menu(self) -> None:
        """Display the main menu."""
        print()
        print("=" * 40)
        print("  AI-Powered Learning Companion")
        print("=" * 40)
        print("1. Generate Questions")
        print("2. Statistics Viewing")
        print("3. Practice Mode")
        print("4. Test Mode")
        print("5. Manage Questions")
        print("6. Quit")
        print("=" * 40)

    # ---------- Generate Questions Mode ----------

    def generate_questions_mode(self) -> None:
        """Handle the Generate Questions mode."""
        print()
        topic = input("Enter a topic (e.g., 'Python Dictionaries'): ").strip()
        if not topic:
            print("Topic cannot be empty.")
            return

        try:
            count_input = input("How many questions? (default 3): ").strip() or "3"
            count = int(count_input)
            if count < 1:
                print("Count must be at least 1. Using default of 3.")
                count = 3
        except ValueError:
            print("Invalid number. Using default of 3.")
            count = 3

        print(f"\nGenerating {count} questions about '{topic}'...")
        try:
            raw_questions = self.llm_client.generate_questions(topic, count)
        except Exception as e:
            print(f"Error generating questions: {e}")
            return

        if not raw_questions:
            print("No questions were generated.")
            return

        accepted = 0
        for raw in raw_questions:
            if not self._is_valid_question(raw):
                print(f"\nSkipping invalid question: {raw}")
                continue

            self._show_raw_question(raw)
            choice = input("[A]ccept / [R]eject / [S]kip rest: ").strip().lower()

            if choice == "s":
                print("Skipping the rest.")
                break
            elif choice == "a":
                question = self._raw_to_question(raw, topic)
                self.quiz_manager.add_question(question)
                accepted += 1
                print(f"✅ Accepted (id={question.id})")
            else:
                print("Rejected.")

        if accepted > 0:
            save_questions(self.quiz_manager.questions, QUESTIONS_FILE)
            print(f"\nSaved {accepted} new question(s) to {QUESTIONS_FILE}.")
        else:
            print("\nNo questions were saved.")


    def statistics_mode(self) -> None:
        """Display statistics for all stored questions."""
        print()
        print("=" * 40)
        print("  Statistics")
        print("=" * 40)

        questions = self.quiz_manager.list_questions()

        if not questions:
            print("No questions stored yet.")
            print("=" * 40)
            return

        total = len(questions)
        active = len([q for q in questions if q.enabled])
        disabled = total - active

        print(f"Total questions: {total}")
        print(f"Active: {active} | Disabled: {disabled}")
        print()

        for q in questions:
            print(q)
            print()

        print("=" * 40)

    def _is_valid_question(self, raw: dict) -> bool:
        """Check if a raw question dict has the required fields."""
        required = {"type", "question", "correct_answer"}
        if not required.issubset(raw.keys()):
            return False
        if raw["type"].upper() == "MCQ" and not raw.get("options"):
            return False
        return True

    def _show_raw_question(self, raw: dict) -> None:
        """Display a raw question dict to the user."""
        print()
        print("=" * 40)
        print(f"Type: {raw['type']}")
        print(f"Question: {raw['question']}")
        if raw["type"].upper() == "MCQ":
            for i, opt in enumerate(raw.get("options", []), 1):
                print(f"  {i}. {opt}")
        print(f"Correct answer: {raw['correct_answer']}")
        print("=" * 40)

    def _raw_to_question(self, raw: dict, topic: str) -> Question:
        """Convert a raw dict to a Question with a new ID."""
        return Question(
            id=self.quiz_manager.get_next_id(),
            type=raw["type"],
            topic=topic,
            question=raw["question"],
            correct_answer=raw["correct_answer"],
            options=raw.get("options"),
            source="LLM",
        )
    


















    