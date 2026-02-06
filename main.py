from fastapi import FastAPI
import sqlite3

app = FastAPI()

# DB connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")
conn.commit()

# ---------------------------
# API 1: Save user (POST)
# ---------------------------
@app.post("/users")
def create_user(name: str, age: int):
    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (name, age)
    )
    conn.commit()
    return {"message": "User saved successfully"}

# ---------------------------
# API 2: Get users (GET)
# ---------------------------
@app.get("/users")
def get_users():
    rows = cursor.execute(
        "SELECT name, age FROM users"
    ).fetchall()
    return [{"name": r[0], "age": r[1]} for r in rows]
