from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_secret_key"


def get_db():
    return sqlite3.connect("expenses.db")


# ---------- CREATE TABLES ----------
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    name TEXT,
    amount INTEGER
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.execute(
    "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    ("admin", "admin123")
)

conn.commit()
conn.close()
def normalize_date(user_date):
    try:
        user_date = user_date.replace('-', '/')
        parts = user_date.split('/')

        if len(parts) != 3:
            return None

        day, month, year = parts
        day = day.zfill(2)
        month = month.zfill(2)

        if len(year) != 4:
            return None

        return f"{year}-{month}-{day}"
    except:
        return None

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = u
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")

#-------signup----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            conn.close()
            return render_template(
                'signup.html',
                error="Username already exists"
            )

    return render_template('signup.html')


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------- HOME ----------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        monthly_expenses=[],
        monthly_total=0
    )

# ---------- ADD EXPENSE ----------
@app.route('/add', methods=['POST'])
def add():
    raw_date = request.form['date']
    name = request.form['name']
    amount = request.form['amount']

    clean_date = normalize_date(raw_date)

    if not clean_date:
        return redirect('/')

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (date, name, amount) VALUES (?, ?, ?)",
        (clean_date, name, amount)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# ---------- MONTHLY ----------
@app.route('/monthly', methods=['POST'])
def monthly():
    month = request.form['month'].zfill(2)
    year = request.form['year']

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE SUBSTR(date, 1, 4) = ?
        AND SUBSTR(date, 6, 2) = ?
    """, (year, month))
    monthly_expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE SUBSTR(date, 1, 4) = ?
        AND SUBSTR(date, 6, 2) = ?
    """, (year, month))
    monthly_total = cur.fetchone()[0] or 0

    # reload main table
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        monthly_expenses=monthly_expenses,
        monthly_total=monthly_total
    )

    
if __name__ == "__main__":
    app.run(debug=True)
