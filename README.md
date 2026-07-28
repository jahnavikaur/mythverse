<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Georgia&size=32&duration=3500&pause=1200&color=D4A5A5&center=true&vCenter=true&width=600&lines=Tales+of+Bharat;A+Mythology+Quiz+Journey;Ramayana+%C2%B7+Mahabharata+%C2%B7+Puranas" alt="Typing SVG" />

⋆｡‍𖦹 ‍⋆ 𓆩♡𓆪 ⋆｡‍𖦹 ‍⋆

**a cozy little quiz world for the stories that raised us**

<br>

![Python](https://img.shields.io/badge/python-3.10+-F7CACA?style=for-the-badge&logo=python&logoColor=white&labelColor=D4A5A5)
![Flask](https://img.shields.io/badge/flask-3.0-EAD7D1?style=for-the-badge&logo=flask&logoColor=white&labelColor=C9A9A6)
![SQLite](https://img.shields.io/badge/sqlite-database-E8C4C4?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=C89191)
![Status](https://img.shields.io/badge/status-in%20bloom-F4DCD6?style=for-the-badge&labelColor=D9AFAF)

</div>

<br>

<div align="center">
  <img width="500" src="https://images.unsplash.com/photo-1544084944-15263ef53152?w=700&auto=format&fit=crop" alt="soft mythology aesthetic banner" />
</div>

<br>

## ˖°𓆩🪷𓆪°˖ · about this project

> *"Every myth is a question the world once asked itself."*

**Tales of Bharat** is a full multi-page Flask site, grown out of a small terminal quiz. It keeps the same six questions from Indian mythology at heart, now wrapped in real accounts, saved scores, a leaderboard, and a JSON API to build on later.

<br>

## ‧₊˚ ⋅ ✧ what it's made of

<div align="center">

| ✦ | feature |
|:---:|:---|
| 🔐 | real password hashing, not plaintext |
| 🏆 | a leaderboard that actually works |
| 🧵 | session-based quiz state — no desyncing between questions |
| 🔗 | a JSON API (`/api/questions`, `/api/leaderboard`) for future apps |

</div>

<br>

## ⋆｡°✩ getting it running

```bash
pip install -r requirements.txt
python init_db.py      # creates the database + seeds the questions
python app.py           # → http://127.0.0.1:5000
```

Then just open the link, make an account, and play ⛅

*(`init_db.py` only needs to run once — `app.py` calls it automatically, so a fresh clone works with just install + run.)*

<br>

## ‧₊˚ folder map ⊹ ࣪ ˖

```
mytho-site/
├── app.py                # routes: auth, quiz flow, results, leaderboard, API
├── config.py              # secret key, DB path, questions-per-round
├── database.py            # SQLite connection + table setup
├── auth.py                 # password hashing (werkzeug)
├── data/
│   └── questions.py        # the question bank — add more here 🌸
├── templates/               # login, quiz, result, leaderboard pages
├── static/css/style.css     # the whole visual vibe lives here
└── init_db.py               # one-time database setup
```

<br>

## 𓂃 ࣪˖ ｡ adding your own questions

Open `data/questions.py` and add another entry in the same shape:

```python
{
    "category": "Ramayana",
    "question": "Your question here?",
    "options": {"a": "...", "b": "...", "c": "...", "d": "..."},
    "correct": "a",
    "difficulty": "medium",
},
```

Then delete `database.db` and rerun `python init_db.py` to reseed. *(back up first if you care about existing scores 🩰)*

<br>

## ⋆⁺₊✧ where this could grow

<div align="center">

| stage | idea |
|:---:|:---|
| 🌱 | timed rounds · difficulty-filtered rounds · daily challenges |
| 🚀 | deploy on Render / Railway / Fly.io, swap SQLite → Postgres |
| 📱 | a React Native / Flutter app on top of the existing API |
| 👯 | head-to-head multiplayer via Flask-SocketIO |

</div>

<br>

## ˚ · . a small note

Set the `QUIZ_SECRET_KEY` environment variable before deploying anywhere public — the default in `config.py` is a dev-only placeholder. And run it with `gunicorn app:app` (or similar) rather than the dev server once it's out in the world.

<br>

<div align="center">

⋆｡‍𖦹 ‍⋆ 𓆩♡𓆪 ⋆｡‍𖦹 ‍⋆

made with patience, chai, and old stories

<img src="https://img.shields.io/badge/-back%20to%20top-EAD7D1?style=flat-square" href="#" />

</div>
