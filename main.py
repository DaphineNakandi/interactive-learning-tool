"""Entry point for the AI Learning Companion."""

import sys

from src.app import App


def run() -> None:
    """Create and run the app."""
    try:
        app = App()
        app.run()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please create a `.env` file with `OPENAI_API_KEY=sk-...`")
        sys.exit(1)


if __name__ == "__main__":
    run()