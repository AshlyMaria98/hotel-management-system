# create_customer_booking.py
from app import app, db
from models import Customer, Booking

with app.app_context():
    print("USING DB:", app.config['SQLALCHEMY_DATABASE_URI'])

    with db.engine.connect() as conn:
        print(">>> Creating Customer table...")
        conn.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS customer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT
            )
        """)

        print(">>> Creating Booking table...")
        conn.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                checkin TEXT,
                checkout TEXT,
                FOREIGN KEY(customer_id) REFERENCES customer(id),
                FOREIGN KEY(room_id) REFERENCES room(id)
            )
        """)

    print("Customer and Booking tables ensured.")
