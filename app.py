from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Create Database
conn = sqlite3.connect('database.db')
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

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username,password)
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

    app.run(debug=True)  all files in single folder so chng ethe pth