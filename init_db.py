"""Run once to set up database.db: creates tables and indexes.
   Also runs automatically every time app.py starts, so this is mainly
   useful if you want to (re)create a fresh DB.

   To load questions, run import_questions.py separately (and again
   any time you add more question files under data/content/).
"""

from database import init_db

if __name__ == "__main__":
    init_db()
    print("Database ready: tables and indexes created.")
    print("Now run `python import_questions.py` to load questions.")