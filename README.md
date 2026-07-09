# Tales of Bharat — Mythology Quiz Site

A proper multi-page Flask site built from the original terminal project.
Same six quiz questions, now wrapped in real accounts, sessions, a score
history, a leaderboard, and a JSON API you can build a mobile app on top
of later.

## Running it locally

```bash
pip install -r requirements.txt
python init_db.py      # creates database.db and seeds the questions
python app.py           # starts the dev server at http://127.0.0.1:5000
```

Open http://127.0.0.1:5000, create an account, and play.

`init_db.py` only needs to be run once — `app.py` also calls it
automatically on startup, so a fresh clone works with just
`pip install` + `python app.py`.

## Project structure

```
mytho-site/
├── app.py                # routes: auth, quiz flow, results, leaderboard, API
├── config.py              # secret key, DB path, questions-per-round
├── database.py            # SQLite connection + table setup
├── auth.py                 # password hashing (werkzeug)
├── data/
│   └── questions.py        # the question bank — add more here
├── templates/               # Jinja2 pages (login, quiz, result, leaderboard)
├── static/css/style.css     # shared visual theme
└── init_db.py               # one-time DB setup script
```

## What changed from the terminal version

- **Real password security** — the original stored passwords in plain
  text. This version hashes them with Werkzeug's `generate_password_hash`.
- **A working leaderboard** — the original had a `leaderboard.html`
  template but no route ever rendered it. It's now wired up and pulls
  real scores from a dedicated `attempts` table (so a user's history
  isn't overwritten every time they play).
- **Session-based quiz state** — question order is shuffled per round
  and tracked server-side, so `next`/`prev` can't desync from the
  actual question index like it could before.
- **A JSON API** (`/api/questions`, `/api/leaderboard`) — same data, in
  case you want to build a separate frontend or a mobile app later
  without touching the quiz logic or database.

## Adding more questions

Open `data/questions.py` and append another entry in the same shape:

```python
{
    "category": "Ramayana",
    "question": "Your question here?",
    "options": {"a": "...", "b": "...", "c": "...", "d": "..."},
    "correct": "a",
    "difficulty": "medium",
},
```

Delete `database.db` and rerun `python init_db.py` to reseed (existing
user accounts and leaderboard history live in the same DB, so back it
up first if you care about them).

`QUESTIONS_PER_ROUND` in `config.py` controls how many questions are
pulled per round — raise it once your question bank is bigger than 6
and rounds will draw a random subset automatically.

## Turning this into "a gaming site" / an app

A few natural next steps, roughly in order of effort:

1. **More game modes** — timed rounds, difficulty-filtered rounds
   (the `difficulty` field is already there), daily challenges.
2. **Deploy it** — Render, Railway, Fly.io, or PythonAnywhere can all
   run this as-is. Swap SQLite for Postgres if you expect concurrent
   writers at scale.
3. **A mobile app** — build a React Native / Flutter client against
   the existing `/api/questions` and `/api/leaderboard` endpoints, and
   add a couple more (`/api/login`, `/api/answer`) using token auth
   instead of cookie sessions.
4. **Multiplayer** — head-to-head rounds would need WebSockets
   (Flask-SocketIO is the natural fit here) to sync two players
   through the same question set in real time.

## Notes

- `SECRET_KEY` defaults to a dev value in `config.py`. Set the
  `QUIZ_SECRET_KEY` environment variable to something random before
  deploying anywhere public.
- The dev server (`python app.py`) is not meant for production traffic
  — use `gunicorn app:app` (or similar) behind a real deployment.
