import sqlite3
import os

# Paths
root_db_path = r"C:\Users\USER\Desktop\hms_project\hotel.db"
instance_db_path = r"C:\Users\USER\Desktop\hms_project\instance\hotel.db"

# Connect to instance DB
conn_instance = sqlite3.connect(instance_db_path)
cur_instance = conn_instance.cursor()

# Fetch all Rooms
cur_instance.execute("SELECT * FROM room;")
rooms = cur_instance.fetchall()

# Fetch all Customers
cur_instance.execute("SELECT * FROM customer;")
customers = cur_instance.fetchall()

conn_instance.close()

# Connect to root DB
conn_root = sqlite3.connect(root_db_path)
cur_root = conn_root.cursor()

# Create room table if not exists
cur_root.execute("""
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT,
    type TEXT,
    price REAL,
    status TEXT
);
""")

# Create customer table if not exists
cur_root.execute("""
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT
);
""")

# Insert Rooms into root DB
for r in rooms:
    cur_root.execute("""
    INSERT OR IGNORE INTO room (id, room_no, type, price, status)
    VALUES (?, ?, ?, ?, ?)
    """, r)

# Insert Customers into root DB
for c in customers:
    cur_root.execute("""
    INSERT OR IGNORE INTO customer (id, name, phone, email, address)
    VALUES (?, ?, ?, ?, ?)
    """, c)

conn_root.commit()
conn_root.close()

print("Migration complete! Rooms and Customers merged into root DB.")
