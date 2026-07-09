# The quiz content itself — same six questions from the original
# add_questions.py, just restructured so each has a category and a
# clean correct_option key (a/b/c/d) instead of a duplicated answer string.
#
# To add more questions later, just append another dict here in the
# same shape. Nothing else in the app needs to change.

QUESTIONS = [
    {
        "category": "Ramayana",
        "question": "Who is the father of Rama?",
        "options": {"a": "Dasharatha", "b": "Krishna", "c": "Shiva", "d": "Brahma"},
        "correct": "a",
        "difficulty": "easy",
    },
    {
        "category": "Mahabharata",
        "question": "Who wrote the Mahabharata?",
        "options": {"a": "Valmiki", "b": "Vyasa", "c": "Tulsidas", "d": "Kalidasa"},
        "correct": "b",
        "difficulty": "easy",
    },
    {
        "category": "Ramayana",
        "question": "Who is Hanuman devoted to?",
        "options": {"a": "Rama", "b": "Krishna", "c": "Shiva", "d": "Indra"},
        "correct": "a",
        "difficulty": "easy",
    },
    {
        "category": "Devas",
        "question": "Who is the god of water?",
        "options": {"a": "Varuna", "b": "Agni", "c": "Vayu", "d": "Surya"},
        "correct": "a",
        "difficulty": "medium",
    },
    {
        "category": "Devas",
        "question": "Who is the god of death?",
        "options": {"a": "Yama", "b": "Agni", "c": "Indra", "d": "Varuna"},
        "correct": "a",
        "difficulty": "medium",
    },
    {
        "category": "Mahabharata",
        "question": "Who lifted Govardhan Hill?",
        "options": {"a": "Krishna", "b": "Balarama", "c": "Indra", "d": "Shiva"},
        "correct": "a",
        "difficulty": "medium",
    },
]


def seed_questions(conn):
    """Insert the question bank if the table is currently empty.
    Safe to call every startup — never duplicates rows."""
    existing = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    if existing > 0:
        return

    for q in QUESTIONS:
        conn.execute(
            """INSERT INTO questions
               (category, question, option_a, option_b, option_c, option_d, correct_option, difficulty)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                q["category"],
                q["question"],
                q["options"]["a"],
                q["options"]["b"],
                q["options"]["c"],
                q["options"]["d"],
                q["correct"],
                q["difficulty"],
            ),
        )
    conn.commit()
