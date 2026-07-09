"""Run once to set up database.db: creates tables and seeds the question bank.
   Also runs automatically every time app.py starts, so this is mainly
   useful if you want a fresh DB or to reseed manually."""

from database import init_db, get_db
from data.questions import seed_questions

if __name__ == "__main__":
    init_db()
    conn = get_db()
    seed_questions(conn)
    conn.close()
    print("Database ready: tables created and questions seeded.")
