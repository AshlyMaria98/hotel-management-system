from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))

    bookings = db.relationship("Booking", backref="customer", cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="customer", cascade="all, delete-orphan")


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20))

    bookings = db.relationship("Booking", backref="room", cascade="all, delete-orphan")


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    checkin = db.Column(db.String(20), nullable=False)
    checkout = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Active")
    payments = db.relationship("Payment", backref="booking", cascade="all, delete-orphan")


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer_name = db.Column(db.String(100))
    room_no = db.Column(db.String(10))
    days = db.Column(db.Integer)
    food = db.Column(db.Float)
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default="Paid")
