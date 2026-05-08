"""
Functions for managing activities.
To run properly, go into the app folder and do
    python3 -m services.activity_service
    or, within the app folder
    import services.activity_service

Activity schema:
- id: int, internal DB id
- email: str, foreign key to user
- title: str
- date: datetime.date
- start_time: datetime.time
- end_time: datetime.time
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
    CREATE TABLE activities (
        id SERIAL,
        email VARCHAR(255),
        title VARCHAR(255),
        date DATE,
        start_time TIME,
        end_time TIME,
        description VARCHAR(1023),
        PRIMARY KEY (id),
        FOREIGN KEY (email) REFERENCES users(email)
    );
    """
    db_execute(query)

if __name__ == "__main__":
    prompt = input("Press enter to initialise activities table. This action assumes no activities table is present.")
    if not prompt:
        init_db()
        print("done")
    else:
        print("doing nothing.")

def create_activity(
    email: str,
    title: str,
    date: dt.date, 
    start_time: dt.time, 
    end_time: dt.time, 
    description: str
):
    """
    Creates a new activity.
    """
    db_execute(
        """
        INSERT INTO activities (
            email, title, date, start_time, end_time, description
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (email, title, date, start_time, end_time, description)
    )

def email_lookup(email: str) -> list:
    """
    Fetches id of all activities under given email.
    returns list of ints
    """
    _, data = db_execute(
        "SELECT id FROM activities WHERE email = %s",
        (email,)
    )

    result = []
    for item in data:
        result.append(item[0])
    return result

def get_activity(id: int) -> list|None:
    """
    Fetches activity info for provided id.
    If activity does not exist, returns None.
    returns {id, email, title, date, start_time, end_time, description}
    """
    _, result = db_execute(
        "SELECT * FROM activities WHERE id = %s",
        (id,)
    )

    if len(result) == 0:
        return None
    else:
        data = result[0]
        headers = ["id", "email", "title", "date", "start_time", "end_time", "description"]
        result = {}
        for name, entry in zip(headers, data):
            result[name] = entry
        
        return result

def delete_activity(id: int):
    """
    Delete activity with the given id
    """
    db_execute(
        """
        DELETE FROM activities WHERE id=%s
        """,
        (id,)
    )

def update_activity(
    id: int,
    title: str,
    date: dt.date, 
    start_time: dt.time, 
    end_time: dt.time, 
    description: str
):
    """
    Updates the existing user that possesses given ID.
    Password is plaintext in this context.
    """
    db_execute(
        """
        UPDATE activities 
        SET 
            title = %s,
            date = %s,
            start_time = %s, 
            end_time = %s,
            description = %s
        WHERE id = %s;
        """,
        (title, date, start_time, end_time, description, id)
    )

def test_module():
    """
    Creates a test event under balls@ball.com.
    """
    email = "balls@ball.com"
    event = {
        "email": email,
        "title": "Balling",
        "date": dt.date.fromisoformat("2026-02-11"), # The browser input gives in this format alr.
        "start_time": dt.time.fromisoformat("06:00"), # Same here
        "end_time": dt.time.fromisoformat("08:00"),
        "description": "Balls balls balls balls"
    }

    print("Creating two copies of event...")
    create_activity(**event)
    create_activity(**event)

    print("Doing lookup of ids under email")
    ids = email_lookup(email)

    print("Deleting one copy")
    delete_activity(ids[-1])
    real_id = ids[-2]

    print("Fetching other copy")
    data = get_activity(real_id)

    print("Editing copy")
    del data["email"]
    del data["id"]
    data["end_time"] = dt.time.fromisoformat("07:00")
    update_activity(real_id, **data)

if __name__ == "__main__":
    print("Running test... Ensure balls@ball.com has an account")
    test_module()