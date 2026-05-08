"""
Functions for managing activities.
To run properly, go into the app folder and do
    python3 -m services.activity_service
    or, within the app folder
    import services.activity_service

Activity schema:
- id: int, internal DB id
- creator_id: int, foreign key to user
- title: str
- date: datetime.date
- start_time: datetime.time
- description: str 
"""

from db import db_execute
import datetime as dt

def init_db():
    """
    Construct table for activities.
    Assumes completely empty postgres installation.
    """
    query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    );
    """
    db_execute(query)

if __name__ == "__main__":
    prompt = input("Press enter to initialise users table. This action assumes no users table is present.")
    if not prompt:
        init_db()

def pw_hash(password: str) -> str:
    """
    Hash the given password with bcrypt.
    Uses a random salt
    """
    data = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(data, salt)
    return str(hashed, encoding = "ascii")

def check_pw(hashed: str, attempt_plain: str) -> bool:
    """
    Pass in a password hash and the plaintext attempt.
    Returns True if matches, False otherwise.
    """
    data = attempt_plain.encode("utf-8")
    return bcrypt.checkpw(data, hashed.encode("ascii"))

def create_user(name: str, email: str, password: str):
    """
    Creates a new user.
    Password is plaintext in this context.
    """
    db_execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, pw_hash(password))
    )

def email_exists(email: str):
    """
    Check if the provided email has a registered account.
    """
    _, result = db_execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    return len(result) > 0

def get_user(email: str) -> list|None:
    """
    Fetches user info for provided email.
    If user does not exist, returns None.
    returns {id, name, email, passsword}
    """
    _, result = db_execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    if len(result) == 0:
        return None
    else:
        user = result[0]
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "password": user[3]
        }