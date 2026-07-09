import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
SECRET_KEY = os.environ.get("QUIZ_SECRET_KEY", "dev-secret-change-me-in-production")

# How many questions make up one round. Currently equal to the full
# question bank size — raise this once you add more questions in
# data/questions.py, and rounds will automatically pull a random subset.
QUESTIONS_PER_ROUND = 6
