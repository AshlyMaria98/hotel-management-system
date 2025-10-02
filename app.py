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

@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        room_id = request.form['room_id']
        checkin = request.form['checkin']
        checkout = request.form['checkout']

        # Optional: Validate dates and input
        if not customer_id or not room_id or not checkin or not checkout:
            flash("All fields are required", "danger")
            return redirect(url_for('bookings'))

        new_booking = Booking(
            customer_id=customer_id,
            room_id=room_id,
            checkin=checkin,
            checkout=checkout
        )
        db.session.add(new_booking)
        db.session.commit()
        flash("Booking added", "success")
        return redirect(url_for('bookings'))

    all_bookings = Booking.query.order_by(Booking.id.desc()).all()
    customers = Customer.query.all()
    rooms = Room.query.all()
    return render_template('bookings.html', bookings=all_bookings, customers=customers, rooms=rooms)


@app.route('/bookings/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(id)
    customers = Customer.query.all()
    rooms = Room.query.all()

    if request.method == 'POST':
        booking.customer_id = request.form['customer_id']
        booking.room_id = request.form['room_id']
        booking.checkin = request.form['checkin']
        booking.checkout = request.form['checkout']

        db.session.commit()
        flash("Booking updated", "success")
        return redirect(url_for('bookings'))

    return render_template('bookings.html', edit_booking=booking, bookings=Booking.query.all(), customers=customers, rooms=rooms)


@app.route('/bookings/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(id)
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


if __name__ == '__main__':
    app.run(debug=True)