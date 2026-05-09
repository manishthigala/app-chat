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


# ================= USER PART =================

@app.route('/')
def home():
    return render_template("index.html")


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


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    return render_template("dashboard.html", user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# ================= ADMIN PART =================

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            return "Invalid Admin Login"

    return """
    <h2>Admin Login</h2>
    <form method="POST">
        <input name="username" placeholder="Admin username"><br><br>
        <input name="password" type="password" placeholder="Admin password"><br><br>
        <button type="submit">Login</button>
    </form>
    """


@app.route('/admin/dashboard')
def admin_dashboard():

    if not session.get('admin'):
        return redirect('/admin')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()

    conn.close()

    html = "<h2>All Users</h2>"

    for u in users:
        html += f"<p>ID: {u[0]} | Username: {u[1]} | Password: {u[2]}</p>"

    html += '<br><a href="/admin/logout">Logout</a>'
    return html


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)
