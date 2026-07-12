"""
Run this ONCE on your existing database.db before/after pulling these updates.

It does two things:
1. Normalizes category names (e.g. "Krishna_leela" -> "Krishna Leela") so
   everything imported under the old naming scheme matches the new one.
2. Removes duplicate question rows (same category + difficulty + question
   text), keeping only the lowest id — this is what causes the same
   question to show up twice in one quiz round.

Safe to run multiple times; it's a no-op once your data is already clean.

Usage:
    python fix_database.py
"""

from database import get_db, init_db


def normalize_categories(conn):
    rows = conn.execute("SELECT DISTINCT category FROM questions").fetchall()
    changed = 0
    for r in rows:
        old = r["category"]
        new = old.replace("_", " ").title()
        if new != old:
            conn.execute(
                "UPDATE questions SET category = ? WHERE category = ?", (new, old)
            )
            changed += 1
    return changed


def remove_duplicates(conn):
    dupes = conn.execute(
        """SELECT category, difficulty, question, MIN(id) AS keep_id, COUNT(*) AS cnt
           FROM questions
           GROUP BY category, difficulty, question
           HAVING cnt > 1"""
    ).fetchall()

    removed = 0
    for d in dupes:
        result = conn.execute(
            """DELETE FROM questions
               WHERE category = ? AND difficulty = ? AND question = ? AND id != ?""",
            (d["category"], d["difficulty"], d["question"], d["keep_id"]),
        )
        removed += result.rowcount
    return removed


def main():
    conn = get_db()

    # Create the base tables first, but the unique index would fail to
    # create if duplicates already exist — so we clean the data BEFORE
    # calling init_db() (which adds that index).
    conn.execute(
        """CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium'
        )"""
    )

    before = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    categories_fixed = normalize_categories(conn)
    duplicates_removed = remove_duplicates(conn)
    conn.commit()
    after = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    print(f"Category names normalized: {categories_fixed}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"Question count: {before} -> {after}")

    # Now safe to add the unique index and any other schema updates.
    init_db()
    print("Indexes verified/created.")


if __name__ == "__main__":
    main()