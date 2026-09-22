"""User interface for the AI Learning Companion."""

from src.quiz_manager import QuizManager
from src.llm_client import LLMClient
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
                print("[Generate Questions — not yet implemented]")
            elif choice == "2":
                print("[Statistics — not yet implemented]")
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