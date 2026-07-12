import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
SECRET_KEY = os.environ.get("QUIZ_SECRET_KEY", "dev-secret-change-me-in-production")

# How many questions make up one round. As long as the selected
# category+difficulty has at least this many questions, a round will
# use exactly this many. If fewer are available, the round uses however
# many exist for that combination.
QUESTIONS_PER_ROUND = 12