from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db   # your models.py has db + tables

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


# ----------------- CUSTOMERS MODULE (Teammate A) -----------------
@app.route('/customers')
def customers():
    return render_template('customers.html')


# ----------------- BOOKINGS MODULE (Teammate B) -----------------
@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


# ----------------- ROOMS MODULE (Teammate C) -----------------
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')


# ----------------- PAYMENTS MODULE (Teammate D) -----------------
@app.route('/payments')
def payments():
    return render_template('payments.html')


# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
