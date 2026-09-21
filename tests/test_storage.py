from src.question import Question
from src.storage import save_questions


question = Question(
    id=1,
    type="MCQ",
    topic="Python",
    question="What is a list?",
    correct_answer="A",
    options=[
        "A collection of items",
        "A function",
        "A loop",
        "A database"
    ]
)

save_questions([question], "data/questions.json")