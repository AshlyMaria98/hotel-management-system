from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db   # your models.py has db + tables
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------- DATABASE SETUP -----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()   # creates all tables defined in models.py


# ----------------- LOGIN / DASHBOARD -----------------
@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin":
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ----------------- CUSTOMERS MODULE -----------------
@app.route('/customers')
def customers():
    return render_template('customers.html')


# ----------------- BOOKINGS MODULE -----------------
@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


# ----------------- ROOMS MODULE -----------------
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')


# ----------------- PAYMENTS MODULE -----------------
DB_NAME = 'hotel.db'

# Initialize DB with new schema
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            amount REAL,
            date TEXT,
            mode TEXT,
            customer_name TEXT,
            customer_id TEXT,
            room_no TEXT,
            days INTEGER,
            food REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# Show all payments
@app.route('/payments')
def payments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM payments ORDER BY id DESC")
    payments = c.fetchall()
    conn.close()
    return render_template('payments.html', view_type='payments', payments=payments)


# Add new payment
@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_id = request.form['customer_id']
        room_no = request.form['room_no']
        days = int(request.form['days'])
        stay = days * 200
        food = days * 500
        total = stay + food
        date = request.form['date']
        mode = request.form['mode']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO payments (booking_id, amount, date, mode, customer_name, customer_id, room_no, days, food)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer_id, total, date, mode, customer_name, customer_id, room_no, days, food))
        conn.commit()
        conn.close()
        return redirect(url_for('payments'))

    return render_template('payments.html', view_type='add')


# Edit payment
@app.route('/payments/edit/<int:id>', methods=['GET', 'POST'])
def edit_payment(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == 'POST':
        booking_id = request.form['booking_id']
        amount = request.form['amount']
        date = request.form['date']
        mode = request.form['mode']
        c.execute(
            "UPDATE payments SET booking_id=?, amount=?, date=?, mode=? WHERE id=?",
            (booking_id, amount, date, mode, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('payments'))

    c.execute("SELECT * FROM payments WHERE id=?", (id,))
    payment = c.fetchone()
    conn.close()
    return render_template('payments.html', view_type='edit', payment=payment)


# Delete payment
@app.route('/payments/delete/<int:id>', methods=['GET', 'POST'])
def delete_payment(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM payments WHERE id=?", (id,))
    payment = c.fetchone()

    if request.method == 'POST':
        c.execute("DELETE FROM payments WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('payments'))

    conn.close()
    return render_template('payments.html', view_type='delete', payment=payment)


# Generate bill
@app.route('/payments/bill/<int:id>')
def bill(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM payments WHERE id=?", (id,))
    payment = c.fetchone()
    conn.close()

    if not payment:
        return "Payment not found", 404

    return render_template('payments.html',
                           view_type='bill',
                           payment_id=payment[0],
                           booking_id=payment[1],
                           amount=payment[2],
                           date=payment[3],
                           mode=payment[4])


if __name__ == '__main__':
    app.run(debug=True)
