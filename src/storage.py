"""File persistence for the AI Learning Companion."""

import json
import os
from typing import List
from datetime import datetime

from src.question import Question


def save_questions(questions: list[Question], file_path: str) -> None:
    """Save questions to a JSON file."""
    question_data = [question.to_dict() for question in questions]

    with open(file_path, "w") as file:
        json.dump(question_data, file, indent=4)


def load_questions(file_path: str) -> list[Question]:
    """
    Load questions from a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A list of Question objects. Empty list if file doesn't exist.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        data = json.load(file)

    return [Question.from_dict(item) for item in data]


def save_result(score: int, total: int, file_path: str) -> None:
    """
    Append a test result to results.txt.

    Args:
        score: Number of correct answers.
        total: Total number of questions.
        file_path: Path to the results.txt file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - Score: {score}/{total}\n"

    with open(file_path, "a") as file:
        file.write(line)


def load_results(file_path: str) -> list[str]:
    """
    Load test results from results.txt.

    Args:
        file_path: Path to the results.txt file.

    Returns:
        A list of result strings. Empty list if file doesn't exist.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]




