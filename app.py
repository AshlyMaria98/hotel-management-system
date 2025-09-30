from models import db   # your models.py has db + tables
import sqlite3
from models import db, Customer, Room, Booking
import datetime
from datetime import datetime as dt
from flask import Flask, render_template, request, redirect, url_for, session, flash



app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------- DATABASE SETUP -----------------

import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotel.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()   # creates all tables defined in models.py

print("USING DB:", app.config["SQLALCHEMY_DATABASE_URI"])
import os
db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
print("FULL PATH DB:", os.path.abspath(db_path))

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
# ----------------- CUSTOMERS MODULE (Teammate: You) -----------------
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Create new customer
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        phone = request.form.get('phone','').strip()
        email = request.form.get('email','').strip()
        address = request.form.get('address','').strip()

        if not name or not phone:
            flash("Name and phone are required", "danger")
            return redirect(url_for('customers'))

        new_c = Customer(name=name, phone=phone, email=email, address=address)
        db.session.add(new_c)
        db.session.commit()
        flash("Customer added", "success")
        return redirect(url_for('customers'))

    # GET: show list + form
    all_customers = Customer.query.order_by(Customer.id.desc()).all()
    return render_template('customers.html', customers=all_customers)


@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    c = Customer.query.get_or_404(id)
    if request.method == 'POST':
        c.name = request.form.get('name','').strip()
        c.phone = request.form.get('phone','').strip()
        c.email = request.form.get('email','').strip()
        c.address = request.form.get('address','').strip()

        if not c.name or not c.phone:
            flash("Name and phone are required", "danger")
            return redirect(url_for('edit_customer', id=id))

        db.session.commit()
        flash("Customer updated", "success")
        return redirect(url_for('customers'))

    # show customers list + prefill edit form
    all_customers = Customer.query.order_by(Customer.id.desc()).all()
    return render_template('customers.html', customers=all_customers, edit_customer=c)


@app.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Customer deleted", "success")
    return redirect(url_for('customers'))



# ----------------- BOOKINGS MODULE -----------------
# ----------------- BOOKINGS MODULE -----------------

@app.route('/bookings')
def bookings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    all_bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template('bookings.html', bookings=all_bookings)

@app.route('/bookings/add', methods=['GET', 'POST'])
def add_booking():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        room_id = request.form.get('room_id')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')

        if not customer_id or not room_id or not checkin or not checkout:
            flash("All fields are required", "danger")
            return redirect(url_for('add_booking'))

        # Check if room is available (optional, but recommended)
        room = Room.query.get(room_id)
        if room.status != 'Available':
            flash("Room is not available", "danger")
            return redirect(url_for('add_booking'))

        # Create booking
        new_booking = Booking(
            customer_id=customer_id,
            room_id=room_id,
            checkin=checkin,
            checkout=checkout
        )
        # Mark room as booked or update status (optional)
        room.status = 'Booked'

        db.session.add(new_booking)
        db.session.commit()
        flash("Booking added", "success")
        return redirect(url_for('bookings'))

    # GET: show form with customers and available rooms
    customers = Customer.query.all()
    rooms = Room.query.filter(Room.status == 'Available').all()
    return render_template('add_booking.html', customers=customers, rooms=rooms)


@app.route('/bookings/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(id)

    if request.method == 'POST':
        booking.customer_id = request.form.get('customer_id')
        booking.room_id = request.form.get('room_id')
        booking.checkin = request.form.get('checkin')
        booking.checkout = request.form.get('checkout')

        db.session.commit()
        flash("Booking updated", "success")
        return redirect(url_for('bookings'))

    customers = Customer.query.all()
    rooms = Room.query.all()
    return render_template('edit_booking.html', booking=booking, customers=customers, rooms=rooms)


@app.route('/bookings/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(id)
    # Optionally, mark room as available again
    room = Room.query.get(booking.room_id)
    if room:
        room.status = 'Available'

    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted", "success")
    return redirect(url_for('bookings'))
# ----------------- ROOMS MODULE -----------------

@app.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)



@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_no = request.form['room_number']
        room_type = request.form['room_type']
        price = request.form['price']
        room_status = request.form['status']   # ✅ fetch status

        new_room = Room(
            room_no=room_no,
            type=room_type,
            price=price,
            status=room_status   # ✅ save status
        )
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('rooms'))
    return render_template('add_room.html')



@app.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    room = Room.query.get_or_404(id)
    if request.method == 'POST':
        room.room_no = request.form['room_number']
        room.type = request.form['room_type']
        room.price = request.form['price']
        room.status = request.form['status']  # Optional
        db.session.commit()
        return redirect(url_for('rooms'))
    return render_template('edit_room.html', room=room)


@app.route('/rooms/delete/<int:id>', methods=['POST'])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('rooms'))

# ----------------- PAYMENTS MODULE -----------------
DB_NAME = 'hotel.db'
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
    payments_list = c.fetchall()
    conn.close()
    return render_template('payments.html', view_type='payments', payments=payments_list)

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