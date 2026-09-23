"""User interface for the AI Learning Companion."""
import random

from src.quiz_manager import QuizManager
from src.llm_client import LLMClient
from src.question import Question
from src.storage import load_questions, save_questions, save_result


QUESTIONS_FILE = "data/questions.json"
RESULTS_FILE = "data/results.txt"


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

            if not choice:
                continue

            if choice == "6":
                print("Goodbye!")
                break
            elif choice == "1":
                self.generate_questions_mode()
            elif choice == "2":
                self.statistics_mode()
            elif choice == "3":
                self.practice_mode()
            elif choice == "4":
                self.test_mode()           
            elif choice == "5":
                self.manage_questions_mode()
            else:
                print("Invalid choice. Please enter 1-6.")

    def practice_mode(self) -> None:
        """Practice mode with weighted question selection."""
        print()
        print("=" * 40)
        print(" Practice Mode")
        print("=" * 40)

        active = self.quiz_manager.get_active_questions()
        if not active:
            print("No active questions. Enable some or generate new ones.")
            return

        while True:
            question = self.quiz_manager.get_weighted_question()
            if question is None:
                break

            correct = self._ask_question(question)

            # Update stats
            question.record_shown()
            if correct:
                question.record_correct()
                print("Correct!")
            else:
                question.record_incorrect()
                print(f"x Incorrect. Correct answer: {question.correct_answer}")

            print(f"Stats: {question.times_correct}/{question.times_shown}"
                  f"({question.get_correct_percentage():.1f}%)")

            again = input("\nContinue practicing? [y/n]: ").strip().lower()
            if again != "y":
                break

        save_questions(self.quiz_manager.questions, QUESTIONS_FILE)
        print("\nProgress saved.")

    def _ask_question(self, question: Question) -> bool:
        """Ask a question and return whether the answer was correct."""
        print()
        print("-" * 40)
        print(f"[{question.id}] ({question.type}) {question.topic}")
        print(f"Q: {question.question}")

        if question.is_mcq():
            options = question.options or []
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            user_answer = input("Your answer: ").strip()

            # If user entered a number, convert to the option text
            if user_answer.isdigit():
                idx = int(user_answer) - 1
                if 0 <= idx < len(options):
                    user_answer = options[idx]

            return question.evaluate_mcq(user_answer)
        else:
            user_answer = input("Your answer: ").strip()
            if not user_answer:
                print("Empty answer - marked incorrect")
                return False
            try:
                return self.llm_client.evaluate_freeform(
                    question.question,
                    question.correct_answer,
                    user_answer,
                )
            except Exception as e:
                print(f"Error evaluating answer: {e}")
                return False

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

    def manage_questions_mode(self) -> None:
        """Let the user enable ordisable questions."""
        print()
        print("=" * 40)
        print("  Manage Questions")
        print("=" * 40)


        if not self.quiz_manager.questions:
            print("No questions stored yet.")
            print("=" * 40)
            return

        while True:
            self._show_compact_list()
            print()

            choice = input("Enter question ID to toggle (or 'q' to quit: ").strip().lower()
            if choice == 'q':
                break

            try:
                question_id = int(choice)
            except ValueError:
                print("Invalid ID. Please enter a number or 'q'.")
                continue

            question = self.quiz_manager.get_question_by_id(question_id)
            if question is None:
                print(f"Question with ID {question_id} not found.")
                continue

            #Show details
            print()
            print("=" * 40)
            print(question)
            print("=" * 40)

            new_state = "Disable" if question.enabled else "Enable"
            confirm = input(f"{new_state} this question? [y/n]: ").strip().lower()
            if confirm != "y":
                print("Cancelled")
                continue

            # Toggle
            if question.enabled:
                self.quiz_manager.disable_question(question_id)
                print(f"Question {question_id} is now DISABLED.")
            else:
                self.quiz_manager.enable_question(question_id)
                print(f"Question {question_id} is now ENABLED.")

            #Save immediately
            save_questions(self.quiz_manager.questions, QUESTIONS_FILE)
            print("Saved.")

    def _show_compact_list(self) -> None:
        """Show a compact table of all questions."""
        print()
        print(f"{'ID':<4} {'Status':<10} {'Type':<10} {'Topic'}")
        print("-" * 50)
        for q in self.quiz_manager.questions:
            status = "Enabled" if q.enabled else "Disabled"
            print(f"{q.id:<4} {status:<10} {q.type:<10} {q.topic}")


    def test_mode(self) -> None:
        """Run a test with random questions and track the score."""
        print()
        print("=" * 40)
        print("  Test Mode")
        print("=" * 40)

        active = self.quiz_manager.get_active_questions()
        if not active:
            print("No active questions. Enable some or generate new ones.")
            return

        total_available = len(active)
        print(f"Active questions available: {total_available}")

        # Ask for count
        try:
            count_input = input(f"How many questions? (1-{total_available}): ").strip()
            count = int(count_input)
            if count < 1 or count > total_available:
                print(f"Invalid count. Must be between 1 and {total_available}.")
                return
        except ValueError:
            print("Invalid number.")
            return

        # Pick random questions without repetition
        selected = random.sample(active, count)

        # Run the test
        score = 0
        for i, question in enumerate(selected, 1):
            print()
            print(f"--- Question {i}/{count} ---")
            correct = self._ask_question(question)

            # Update stats
            question.record_shown()
            if correct:
                question.record_correct()
                score += 1
            else:
                question.record_incorrect()

        # Show final score
        print()
        print("=" * 40)
        print(f"Test complete! You answered {score}/{count} correctly.")
        print("=" * 40)

        # Save result and questions
        save_result(score, count, RESULTS_FILE)
        save_questions(self.quiz_manager.questions, QUESTIONS_FILE)
        print(f"Result saved to {RESULTS_FILE}.")

















