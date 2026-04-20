from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# INTENTIONALLY VULNERABLE: hard-coded secret key (SonarCloud should flag this)
app.config['SECRET_KEY'] = 'hardcoded-secret-for-demo'

# Database path (we won't actually use it for tests; it's here for vulnerability demo)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lms.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return jsonify({"message": "LMS backend is running"})


@app.route("/users")
def get_user():
    """
    INTENTIONALLY VULNERABLE EXAMPLE FOR SONARCLOUD:
    Builds an SQL query by concatenating user input directly.
    """
    username = request.args.get("username", "")

    conn = get_db_connection()
    cur = conn.cursor()

    # SQL injection vulnerability: user input is directly concatenated into the query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cur.execute(query)
        rows = [dict(row) for row in cur.fetchall()]
    except sqlite3.Error:
        # If the DB doesn't exist or query fails, just return empty list
        rows = []
    finally:
        conn.close()

    return jsonify(rows)


@app.route("/search")
def search():
    """
    INTENTIONALLY VULNERABLE EXAMPLE FOR ZAP:
    Reflects the 'q' parameter directly into HTML without escaping.
    ZAP should detect reflected XSS here.
    """
    q = request.args.get("q", "")
    return f"<html><body>Results for: {q}</body></html>"


if __name__ == "__main__":
    # For local testing: python app.py
    app.run(debug=True)
