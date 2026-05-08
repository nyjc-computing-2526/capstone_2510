"""
Functions for managing users.
To run properly, go into the app folder and do
    python3 -m services.auth_service

User schema:
- id: int, internal DB id
- name: str, name of user. 
    - Advise users to include (XXXX) where X is a number for class.
- email: str
- password: str
"""

from db import db_execute

def init_db():
    """
    Construct table for users.
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

def create_user(name: str, email: str, password: str):
    """
    Creates a new user.
    """
    db_execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )

def email_exists(email):
    """
    Check if the provided email has a registered account.
    """
    _, result = db_execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    return len(result) > 0

def get_user(email):
    """
    Fetches user info for provided email.
    Make sure that the email is actually registered.
    """
    _, result = db_execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    return result[0]