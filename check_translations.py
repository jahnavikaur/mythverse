"""check_translations.py — finds translation problems before users do.

Run:  python check_translations.py

It checks that:
  1. every entry in translations.py has non-empty text for every language
  2. every translate('key') used in templates/ and app.py exists in translations.py
  3. every domain in the questions database has a translated name
"""
import re
import sqlite3
from pathlib import Path

from config import DATABASE
from translations import UI_TEXT, SUPPORTED_LANGUAGES

ROOT = Path(__file__).parent
problems = 0

# 1. Missing / empty language text
for key, texts in UI_TEXT.items():
    for lang in SUPPORTED_LANGUAGES:
        if not (texts.get(lang) or "").strip():
            print(f"[EMPTY]   '{key}' has no '{lang}' text")
            problems += 1

# 2. Keys used in code but not defined
used = {}
for path in list(ROOT.glob("templates/*.html")) + [ROOT / "app.py"]:
    for key in re.findall(r"""translate\(\s*['"](\w+)['"]\s*[,)]""", path.read_text(encoding="utf-8")):
        used.setdefault(key, path.name)
for key, where in sorted(used.items()):
    if key not in UI_TEXT:
        print(f"[UNKNOWN] '{key}' is used in {where} but not defined in translations.py")
        problems += 1

# 3. Domains in the database without a translated name
try:
    conn = sqlite3.connect(DATABASE)
    for (cat,) in conn.execute("SELECT DISTINCT category FROM questions"):
        if f"domain_{cat}" not in UI_TEXT:
            print(f"[DOMAIN]  database domain '{cat}' has no 'domain_{cat}' entry in translations.py")
            problems += 1
    conn.close()
except sqlite3.Error as e:
    print(f"(skipped database check: {e})")

print("All translations OK ✔" if problems == 0 else f"\n{problems} problem(s) found.")