from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from datetime import datetime
import csv
import io

app = Flask(__name__)

def init_db():
    """Initialize the SQLite database."""
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
    if request.method == "POST":
        symptom = request.form.get("symptom")
        severity = request.form.get("severity")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO symptoms (date, symptom, severity) VALUES (?, ?, ?)",
                         (date, symptom, severity))

        return redirect("/")

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, date, symptom, severity FROM symptoms ORDER BY date DESC")
        logs = cur.fetchall()

    return render_template("index.html", logs=logs)

@app.route("/export")
def export_csv():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT date, symptom, severity FROM symptoms ORDER BY date DESC")
        logs = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Symptom", "Severity"])
    writer.writerows(logs)
    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     download_name="symptom_logs.csv",
                     as_attachment=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
