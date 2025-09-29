import sqlite3

db_path = "hotel.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in DB:")
for table in tables:
    print("-", table[0])

print("\n---\n")

# Step 2: Show columns for each table
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"Columns in {table_name}:")
    for col in columns:
        print("   ", col)
    print("\n")

# Step 3: Show all rows for each table
for table in tables:
    table_name = table[0]
    print(f"Contents of {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print("   ", row)
    print("\n")

conn.close()
