import sqlite3

db_path = "hotel.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Room table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT NOT NULL,
    type TEXT NOT NULL,
    price REAL NOT NULL,
    status TEXT DEFAULT 'Available'
)
""")
print("Room table ensured with status column.")

conn.commit()
conn.close()
