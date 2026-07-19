import sqlite3
from config import DATABASE


def get_db():
    """Open a new connection with row access by column name."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables and indexes if they don't already exist. Safe to call every startup."""
    conn = get_db()
    conn.execute("PRAGMA journal_mode=WAL")  # better read/write concurrency at scale
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium'
        );

        -- Speeds up "give me N random questions from category X at difficulty Y"
        CREATE INDEX IF NOT EXISTS idx_category_difficulty
            ON questions(category, difficulty);

        -- Prevents duplicate rows when import_questions.py is re-run
        CREATE UNIQUE INDEX IF NOT EXISTS idx_question_unique
            ON questions(category, difficulty, question);

        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    conn.commit()

    # Add Hindi translation columns if they don't exist yet. SQLite has no
    # "ADD COLUMN IF NOT EXISTS", so check first. English columns remain
    # the required/canonical fields; these are nullable and optional.
    existing_cols = {r["name"] for r in conn.execute("PRAGMA table_info(questions)").fetchall()}
    hindi_columns = ["question_hi", "option_a_hi", "option_b_hi", "option_c_hi", "option_d_hi"]
    for col in hindi_columns:
        if col not in existing_cols:
            conn.execute(f"ALTER TABLE questions ADD COLUMN {col} TEXT")
    conn.commit()
    conn.close()