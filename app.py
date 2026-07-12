import random
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

from config import SECRET_KEY, QUESTIONS_PER_ROUND
from database import get_db, init_db
from auth import hash_password, verify_password

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Score-based titles, checked top to bottom against percentage correct.
TIERS = [
    (0.9, "Avatar", "A rare, near-perfect command of the epics."),
    (0.7, "Maharishi", "A great sage's grasp of the old stories."),
    (0.5, "Yodha", "A warrior's knowledge — solid, with room to grow."),
    (0.0, "Shishya", "A student's beginning. Every sage started here."),
]


def tier_for(score, total):
    pct = (score / total) if total else 0
    for threshold, title, desc in TIERS:
        if pct >= threshold:
            return title, desc
    return TIERS[-1][1], TIERS[-1][2]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home"))
        return view(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------- pages ----

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("setup"))
    return render_template("login.html")


@app.route("/setup", methods=["GET", "POST"])
@login_required
def setup():
    conn = get_db()
    counts = conn.execute(
        "SELECT category, difficulty, COUNT(*) AS cnt "
        "FROM questions GROUP BY category, difficulty"
    ).fetchall()
    conn.close()

    if not counts:
        flash("No questions available yet. Import some questions first.")
        return render_template("setup.html", categories=[], difficulty_order=[], counts={})

    categories = sorted({r["category"] for r in counts})
    order = {"easy": 0, "medium": 1, "hard": 2}
    difficulties = sorted({r["difficulty"] for r in counts}, key=lambda d: order.get(d, 99))
    count_map = {(r["category"], r["difficulty"]): r["cnt"] for r in counts}

    if request.method == "POST":
        category = request.form.get("category")
        difficulty = request.form.get("difficulty")

        if (category, difficulty) not in count_map:
            flash("Please pick a valid domain and difficulty combination.")
            return redirect(url_for("setup"))

        # Starting a new round — clear any in-progress quiz state.
        for key in ("quiz_ids", "quiz_index", "quiz_score", "quiz_saved", "quiz_answered"):
            session.pop(key, None)
        session["quiz_category"] = category
        session["quiz_difficulty"] = difficulty
        return redirect(url_for("play"))

    return render_template(
        "setup.html", categories=categories, difficulty_order=difficulties, counts=count_map
    )


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Enter both a username and password.")
        return redirect(url_for("home"))

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        conn.close()
        flash("That username is already taken.")
        return redirect(url_for("home"))

    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hash_password(password)),
    )
    conn.commit()
    conn.close()
    flash("Account created — log in below.")
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("play"))

    flash("Invalid username or password.")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/play")
@login_required
def play():
    if "quiz_category" not in session or "quiz_difficulty" not in session:
        return redirect(url_for("setup"))

    if "quiz_ids" not in session:
        conn = get_db()
        rows = conn.execute(
            "SELECT id FROM questions WHERE category = ? AND difficulty = ?",
            (session["quiz_category"], session["quiz_difficulty"]),
        ).fetchall()
        conn.close()
        ids = [r["id"] for r in rows]
        random.shuffle(ids)
        # ids are unique primary keys pulled from a single filtered query,
        # so slicing a shuffled list can never repeat a question in one round.
        session["quiz_ids"] = ids[:QUESTIONS_PER_ROUND]
        session["quiz_index"] = 0
        session["quiz_score"] = 0
        session["quiz_saved"] = False
        session.pop("quiz_answered", None)

    ids = session["quiz_ids"]
    index = session["quiz_index"]

    if index >= len(ids):
        return redirect(url_for("result"))

    conn = get_db()
    q = conn.execute("SELECT * FROM questions WHERE id = ?", (ids[index],)).fetchone()
    conn.close()

    answered = session.get("quiz_answered")

    return render_template(
        "quiz.html",
        question=q,
        index=index,
        total=len(ids),
        score=session["quiz_score"],
        answered=answered,
    )


@app.route("/answer", methods=["POST"])
@login_required
def answer():
    if session.get("quiz_answered"):
        # Already answered this question — ignore resubmits (e.g. back button).
        return redirect(url_for("play"))

    selected = request.form.get("option")
    ids = session.get("quiz_ids", [])
    index = session.get("quiz_index", 0)

    if index >= len(ids):
        return redirect(url_for("result"))

    conn = get_db()
    q = conn.execute("SELECT * FROM questions WHERE id = ?", (ids[index],)).fetchone()
    conn.close()

    correct = selected == q["correct_option"]
    if correct:
        session["quiz_score"] = session.get("quiz_score", 0) + 1

    session["quiz_answered"] = {
        "selected": selected,
        "correct": correct,
        "correct_option": q["correct_option"],
    }
    return redirect(url_for("play"))


@app.route("/next")
@login_required
def next_question():
    session["quiz_index"] = session.get("quiz_index", 0) + 1
    session.pop("quiz_answered", None)
    return redirect(url_for("play"))


@app.route("/result")
@login_required
def result():
    ids = session.get("quiz_ids", [])
    score = session.get("quiz_score", 0)
    total = len(ids)

    if total and not session.get("quiz_saved"):
        conn = get_db()
        conn.execute(
            "INSERT INTO attempts (user_id, username, score, total) VALUES (?, ?, ?, ?)",
            (session["user_id"], session["username"], score, total),
        )
        conn.commit()
        conn.close()
        session["quiz_saved"] = True

    title, desc = tier_for(score, total) if total else ("", "")
    return render_template("result.html", score=score, total=total, title=title, desc=desc)


@app.route("/play/reset")
@login_required
def reset_quiz():
    for key in ("quiz_ids", "quiz_index", "quiz_score", "quiz_saved", "quiz_answered",
                "quiz_category", "quiz_difficulty"):
        session.pop(key, None)
    return redirect(url_for("setup"))


@app.route("/leaderboard")
def leaderboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT username, score, total, created_at FROM attempts "
        "ORDER BY score DESC, created_at ASC LIMIT 10"
    ).fetchall()
    conn.close()
    return render_template("leaderboard.html", rows=rows)


# ------------------------------------------------- JSON API (for the app) --
# Same game state, exposed as JSON. A future mobile client (React Native,
# Flutter, etc.) can talk to these endpoints instead of the HTML pages —
# nothing about the quiz logic or database needs to change.

@app.route("/api/questions")
def api_questions():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, category, question, option_a, option_b, option_c, option_d, difficulty "
        "FROM questions"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/leaderboard")
def api_leaderboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT username, score, total, created_at FROM attempts "
        "ORDER BY score DESC, created_at ASC LIMIT 20"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)