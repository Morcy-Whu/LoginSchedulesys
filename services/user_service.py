from werkzeug.security import generate_password_hash, check_password_hash
from db import execute, fetch_one

def create_user(username, password):
    password_hash = generate_password_hash(password)
    execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

def authenticate_user(username, password):
    user = fetch_one(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None

def delete_user(user_id):
    execute("DELETE FROM users WHERE id = ?", (user_id,))
