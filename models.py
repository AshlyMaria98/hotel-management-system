# Import db if not already
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# --- Customer Model ---
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Relationship: one customer can have many bookings
    bookings = db.relationship('Booking', backref='customer', lazy=True)

# --- Room Model ---
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(20))
    type = db.Column(db.String(50))
    status = db.Column(db.String(20))
    # Relationship: one room can have many bookings
    bookings = db.relationship('Booking', backref='room', lazy=True)

# --- Booking Model ---
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    checkin = db.Column(db.Date)
    checkout = db.Column(db.Date)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    date = db.Column(db.String(20))