"""LLM client for generating and evaluating questions."""

import os
import json
from typing import List

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    """Handles all communication with the OpenAI API."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        """Initialize the LLM client."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_questions(self, topic: str, count: int = 3) -> list[dict]:
        """Generate questions about a topic using the LLM."""
        prompt = f"""You are a quiz question generator.

Generate exactly {count} questions about "{topic}".

Include a mix of:
- Multiple choice (MCQ) with 4 options
- Freeform with a reference answer

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "type": "MCQ",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "..."
    }},
    {{
      "type": "freeform",
      "question": "...",
      "correct_answer": "..."
    }}
  ]
}}

No text before or after the JSON."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}\n\nRaw response:\n{content}")

        return data["questions"]

    def evaluate_freeform(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
    ) -> bool:
        """Evaluate a user's freeform answer using the LLM."""
        prompt = f"""You are evaluating a student's answer.

Question: {question}
Reference answer: {correct_answer}
Student's answer: {user_answer}

Is the student's answer correct? Reply with ONLY the word "Correct" or "Incorrect"."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip().lower()

        if content.startswith("incorrect"):
            return False
        if content.startswith("correct"):
            return True
        return False