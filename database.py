import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (email, password)
VALUES (?, ?)
""", (
    "supplychain.project.ai@gmail.com",
    "35693569"
))

conn.commit()

conn.close()

print("Database created successfully.")