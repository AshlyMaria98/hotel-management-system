# create_payment_table.py
from app import app, db
from models import Payment

with app.app_context():
    print("USING DB:", app.config['SQLALCHEMY_DATABASE_URI'])

    with db.engine.connect() as conn:
        print(">>> Creating Payments table...")
        conn.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER,
                customer_id INTEGER,
                customer_name TEXT,
                room_no TEXT,
                days INTEGER,
                food REAL,
                amount REAL,
                date TEXT,
                payment_method TEXT,
                FOREIGN KEY(booking_id) REFERENCES booking(id)
            )
        """)

    print("Payments table ensured.")
