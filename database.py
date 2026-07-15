import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

email = os.getenv("APP_EMAIL")
password = os.getenv("APP_PASSWORD")

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute(
    """
    INSERT OR IGNORE INTO users (email, password)
    VALUES (?, ?)
    """,
    (email, password)
)

conn.commit()

conn.close()

print("Database created successfully.")