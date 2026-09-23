# AI-Powered Learning Companion

A text-based study tool that uses an LLM (OpenAI GPT) to **generate quiz questions** on any topic, **evaluate freeform answers**, and **track your progress** over time.

Built as the final project for Turing College's "Professional Python Practices" sprint.

## Features

- **Generate Questions** — Enter a topic (e.g., "Python Dictionaries") and the LLM generates multiple-choice and freeform questions in a structured JSON format.
- **Review Before Saving** — Accept, reject, or skip each generated question before it's stored.
- **Practice Mode** — Weighted random selection: questions you get wrong appear more often.
- **Test Mode** — Pick N random questions, no repetition. Score is saved to `results.txt`.
- **Statistics** — See every question with ID, topic, type, enabled status, and correct answer percentage.
- **Manage Questions** — Enable or disable questions by ID. Disabled questions don't appear in Practice or Test.

## Architecture

```
interactive-learning-tool/
├── main.py                    # Entry point — runs the App
├── src/
│   ├── app.py                 # CLI + all mode handlers
│   ├── question.py            # Question data model
│   ├── quiz_manager.py        # Manages the collection of questions
│   ├── llm_client.py          # OpenAI API wrapper
│   └── storage.py             # JSON + text file persistence
├── data/
│   ├── questions.json         # Stored questions + stats
│   └── results.txt            # Test results log
├── tests/                     # Unit tests (pytest)
├── .env                       # API key (NOT committed)
├── .gitignore
└── requirements.txt
```

### Class Responsibilities

| Class | Responsibility |
|-------|----------------|
| `Question` | Represents ONE question (MCQ or freeform) with its stats. |
| `QuizManager` | Manages the COLLECTION of questions — add, find, enable/disable, weighted selection. |
| `LLMClient` | Talks to the OpenAI API — generates questions and evaluates freeform answers. |
| `App` | The CLI — menu loop, mode handlers, user input. |
| `storage` | Read/write JSON and text files. |

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

   **Important:** `.env` is in `.gitignore` — your key will never be committed.

## Running

```bash
python main.py
```

Then choose from the menu:
```
1. Generate Questions
2. Statistics Viewing
3. Practice Mode
4. Test Mode
5. Manage Questions
6. Quit
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest --cov=src
```

The LLM tests use `pytest-mock` so they don't make real API calls.

## Technical Highlights

- **Object-Oriented Design** — Clear separation between `Question`, `QuizManager`, `LLMClient`, and `App`.
- **API Key Security** — Loaded from `.env` via `python-dotenv`; `.env` is gitignored.
- **Structured LLM Output** — Uses OpenAI's `response_format={"type": "json_object"}` to guarantee valid JSON.
- **Weighted Random Selection** — Questions with lower correct percentages appear more often in Practice Mode.
- **Fail-Closed Freeform Evaluation** — If the LLM returns an unexpected response, we mark the answer incorrect by default.
- **Regression Tests** — Bugs found during development are locked in with tests.

## Design Decisions & Trade-offs

- **JSON over CSV** for questions — options are a list; JSON handles nested structures naturally.
- **Mocked LLM tests** — Fast, free, deterministic; manual REPL testing covers real integration.
- **No GUI** — CLI is faster to build and easier to test; the project's learning goals are Python-focused.

## Author

Daphine Nakandi

## Acknowledgements

- Turing College — for the sprint structure and review format
- OpenAI — for the GPT API

## Related Projects

Previous hands-on exercise (D&D Combat Game refactor):
https://github.com/DaphineNakandi/dnd-combat