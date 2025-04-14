from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    """Initialize the SQLite database (if not already)."""
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                symptom TEXT NOT NULL,
                severity INTEGER
            )
        ''')

@app.route("/", methods=["GET", "POST"])
def index():
    # If user submitted the form, insert a new log entry
    if request.method == "POST":
        symptom = request.form.get("symptom")
        severity = request.form.get("severity")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO symptoms (date, symptom, severity) VALUES (?, ?, ?)",
                         (date, symptom, severity))

        return redirect("/")

    # Otherwise, retrieve all entries and display them
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, date, symptom, severity FROM symptoms ORDER BY date DESC")
        logs = cur.fetchall()

    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
