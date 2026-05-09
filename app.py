from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Create Database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

# Login
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    session['user'] = username

    return redirect('/dashboard')

# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    return render_template(
        "dashboard.html",
        user=session['user']
    )

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
