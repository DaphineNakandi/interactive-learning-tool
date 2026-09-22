"""Tests for LLMClient (using mocks — no real API calls)."""

import json
import pytest

from src.llm_client import LLMClient


@pytest.fixture
def client(monkeypatch):
    """Create an LLMClient with a fake API key."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")
    return LLMClient()


def test_generate_questions_parses_json(client, mocker):
    """Test that generate_questions parses the LLM's JSON response."""
    fake_response = {
        "questions": [
            {
                "type": "MCQ",
                "question": "What is 2+2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4",
            }
        ]
    }

    # Mock the OpenAI response
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content=json.dumps(fake_response)))
    ]

    mocker.patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_completion,
    )

    questions = client.generate_questions("Math", count=1)

    assert len(questions) == 1
    assert questions[0]["type"] == "MCQ"
    assert questions[0]["correct_answer"] == "4"


def test_evaluate_freeform_correct(client, mocker):
    """Test that evaluate_freeform returns True when LLM says 'Correct'."""
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="Correct"))
    ]

    mocker.patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_completion,
    )

    result = client.evaluate_freeform("Q?", "A", "A")
    assert result is True


def test_evaluate_freeform_incorrect(client, mocker):
    """Test that evaluate_freeform returns False when LLM says 'Incorrect'."""
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="Incorrect"))
    ]

    mocker.patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_completion,
    )

    result = client.evaluate_freeform("Q?", "A", "B")
    assert result is False


def test_evaluate_freeform_handles_incorrect_substring(client, mocker):
    """Test that 'Incorrect' is not mistakenly read as 'Correct'."""
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="Incorrect"))
    ]

    mocker.patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_completion,
    )

    result = client.evaluate_freeform("Q?", "A", "wrong")
    # If we had a naive `"correct" in response` check, this would be True.
    assert result is False


def test_evaluate_freeform_unexpected_response(client, mocker):
    """Test that unexpected responses default to False (fail closed)."""
    mock_completion = mocker.Mock()
    mock_completion.choices = [
        mocker.Mock(message=mocker.Mock(content="Maybe?"))
    ]

    mocker.patch.object(
        client.client.chat.completions,
        "create",
        return_value=mock_completion,
    )

    result = client.evaluate_freeform("Q?", "A", "?")
    assert result is False



    