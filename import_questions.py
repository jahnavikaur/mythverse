"""
Reads every question file under data/content/<difficulty>/<domain>.json
and inserts them into database.db.

Safe to run again and again as you add more files or more questions to
existing files — duplicates (same category + difficulty + question text)
are silently skipped thanks to the unique index on the questions table.

Usage:
    python import_questions.py
"""

import json
from pathlib import Path

from database import get_db, init_db

CONTENT_DIR = Path(__file__).parent / "data" / "content"
REQUIRED_KEYS = {"question", "options", "correct"}
REQUIRED_OPTION_KEYS = {"a", "b", "c", "d"}


def text_of(field, lang):
    """A field can be a plain string (English-only, old format) or a
    {'en': ..., 'hi': ...} dict (bilingual, new format). Returns '' if
    that language isn't present."""
    if isinstance(field, str):
        return field.strip() if lang == "en" else ""
    if isinstance(field, dict):
        return (field.get(lang) or "").strip()
    return ""


def load_content_files():
    """Walk data/content/<difficulty>/<domain>.json and yield validated rows."""
    if not CONTENT_DIR.exists():
        raise SystemExit(f"No content directory found at {CONTENT_DIR}")

    for difficulty_dir in sorted(CONTENT_DIR.iterdir()):
        if not difficulty_dir.is_dir():
            continue
        difficulty = difficulty_dir.name  # "easy" / "medium" / "hard"

        for domain_file in sorted(difficulty_dir.glob("*.json")):
            # "ramayana.json" -> "Ramayana", "krishna_leela.json" -> "Krishna Leela"
            category = domain_file.stem.replace("_", " ").title()

            try:
                items = json.loads(domain_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(f"  SKIPPING {domain_file} — invalid JSON: {e}")
                continue

            for i, q in enumerate(items):
                problem = validate_question(q)
                if problem:
                    print(f"  SKIPPING {domain_file} item #{i} — {problem}")
                    continue

                opts = q["options"]
                yield (
                    category,
                    text_of(q["question"], "en"),
                    text_of(q["question"], "hi"),
                    text_of(opts["a"], "en"), text_of(opts["a"], "hi"),
                    text_of(opts["b"], "en"), text_of(opts["b"], "hi"),
                    text_of(opts["c"], "en"), text_of(opts["c"], "hi"),
                    text_of(opts["d"], "en"), text_of(opts["d"], "hi"),
                    q["correct"].lower(),
                    difficulty,
                )


def validate_question(q):
    """Return a description of what's wrong, or None if the question is valid."""
    if not isinstance(q, dict) or not REQUIRED_KEYS.issubset(q):
        return f"missing required keys (need {REQUIRED_KEYS})"
    if not isinstance(q.get("options"), dict) or not REQUIRED_OPTION_KEYS.issubset(q["options"]):
        return "options must have keys a, b, c, d"
    if q["correct"].lower() not in REQUIRED_OPTION_KEYS:
        return f"correct option '{q['correct']}' is not one of a/b/c/d"
    if not text_of(q["question"], "en"):
        return "empty English question text (English is required; Hindi is optional)"
    for letter in REQUIRED_OPTION_KEYS:
        if not text_of(q["options"][letter], "en"):
            return f"empty English text for option '{letter}'"
    return None


def main():
    init_db()  # make sure tables + indexes exist before importing
    rows = list(load_content_files())

    if not rows:
        print("No valid questions found. Nothing imported.")
        return

    conn = get_db()
    before = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    conn.executemany(
        """INSERT OR IGNORE INTO questions
           (category, question, question_hi,
            option_a, option_a_hi, option_b, option_b_hi,
            option_c, option_c_hi, option_d, option_d_hi,
            correct_option, difficulty)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()

    after = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    print(f"\nRead {len(rows)} question(s) from JSON files.")
    print(f"Inserted {after - before} new question(s) (duplicates skipped).")
    print(f"Total questions in database.db: {after}")


if __name__ == "__main__":
    main()