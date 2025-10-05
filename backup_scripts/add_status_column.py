# add_status_column.py

from app import app, db
from sqlalchemy import text  # ✅ import text

with app.app_context():
    table_name = 'payments'
    new_column = 'status'

    with db.engine.connect() as conn:
        # Get existing columns safely
        result = conn.execute(text(f"PRAGMA table_info({table_name});"))
        existing_columns = [row['name'] for row in result.mappings()]

        if new_column in existing_columns:
            print(f"Column '{new_column}' already exists in '{table_name}' table.")
        else:
            # Add the column safely
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {new_column} VARCHAR(20) DEFAULT 'Paid';"))
            print(f"Column '{new_column}' added successfully to '{table_name}' table.")
