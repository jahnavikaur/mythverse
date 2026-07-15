"""
Run this any time you suspect duplicate or misspelled categories in
database.db — e.g. after renaming a JSON file, fixing a typo in a domain
name, or re-running import_questions.py after such a change.

What it does, in order (order matters — do not rearrange):
  1. Drops the unique index temporarily (renames below would otherwise
     collide with rows that already exist under the correct name).
  2. Applies known category renames (see CATEGORY_RENAMES below — add to
     this dict any time you fix a typo'd filename).
  3. Applies generic normalization (underscores -> spaces, Title Case)
     for anything not explicitly listed.
  4. Removes exact duplicate rows (same category + difficulty + question),
     keeping the lowest id.
  5. Recreates the unique index now that the data is clean.

Safe to run repeatedly — it's a no-op once everything is already clean.

Usage:
    python fix_database.py
"""

from database import get_db, init_db

# Add an entry here any time you fix a typo in a JSON filename/category,
# so old rows imported under the wrong name get merged into the right one.
CATEGORY_RENAMES = {
    "Mahabharat": "Mahabharata",
    "Krishan Leela": "Krishna Leela",
}


def apply_known_renames(conn):
    changed = 0
    for old, new in CATEGORY_RENAMES.items():
        result = conn.execute(
            "UPDATE questions SET category = ? WHERE category = ?", (new, old)
        )
        if result.rowcount:
            print(f"  Renamed {result.rowcount} row(s): '{old}' -> '{new}'")
            changed += result.rowcount
    return changed


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
            print(f"  Normalized: '{old}' -> '{new}'")
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

    # The unique index would block renames that collide with existing
    # rows, so drop it first and recreate it only once data is clean.
    conn.execute("DROP INDEX IF EXISTS idx_question_unique")
    conn.commit()

    before = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    print("Applying known category renames...")
    renamed = apply_known_renames(conn)
    conn.commit()

    print("Normalizing any remaining underscore/casing issues...")
    normalized = normalize_categories(conn)
    conn.commit()

    print("Removing exact duplicate questions...")
    duplicates_removed = remove_duplicates(conn)
    conn.commit()

    after = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    # Recreate indexes now that the data is clean.
    init_db()

    print()
    print(f"Rows affected by known renames: {renamed}")
    print(f"Categories auto-normalized: {normalized}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"Question count: {before} -> {after}")
    print()
    print("Current breakdown:")
    for r in conn.execute(
        "SELECT category, difficulty, COUNT(*) c FROM questions "
        "GROUP BY category, difficulty ORDER BY category, difficulty"
    ).fetchall():
        print(f"  {r['category']:20} {r['difficulty']:8} {r['c']}")

    conn.close()


if __name__ == "__main__":
    main()