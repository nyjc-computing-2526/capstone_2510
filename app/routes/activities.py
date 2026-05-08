from flask import request, session, redirect
from services.render import render_template
import services.activity_service as activity
from app_obj import app
import datetime as dt
from typing import Callable
import sqlite3

def require_login(inner_fn: Callable):
    """
    Decorator function around a route.
    Adding it makes the route redirect user to login page if not logged in.
    Effectively disables access to those paths.
    """
    def route(*args, **kwargs):
        nonlocal inner_fn
        if "logged_in" not in session:
            return redirect("/")
        else:
            return inner_fn(*args, **kwargs)
    route.__name__ = inner_fn.__name__ # Carry over so that url_for works
    return route

@app.route('/activities')
@require_login
def activities():
    """
    Render page that shows all activities.
    """
    email = session["email"]
    ids = activity.email_lookup(email)

    headers = ["id", "title", "date", "start_time", "end_time", "description"]

    entries = []
    for id in ids:
        data = activity.get_activity(id)
        data["date"] = str(data["date"])
        data["start_time"] = str(data["start_time"])
        data["end_time"] = str(data["end_time"])

        entry = []
        for header in headers:
            entry.append(data[header])
        entries.append(entry)

    return render_template("activities/activities.html", entries = entries)

def valid_create(task_name, description) -> bool:
    """
    Validate an activity to be created.
    Checks task_name and description only for now.
    """
    if type(task_name) != str or task_name == "":
        return False
    if type(description) != str or description == "":
        return False
    return True

@app.route('/activities/create', methods = ["GET", "POST"])
def create_activity():
    if request.method == "POST":
        data = {
            "email": session["email"],
            "title": request.form["title"],
            "date": dt.date.fromisoformat(request.form["date"]), 
            "start_time": dt.time.fromisoformat(request.form["start_time"]),
            "end_time": dt.time.fromisoformat(request.form["end_time"]),
            "description": request.form["description"]
        }

        valid = valid_create(data["title"], data["description"])
        if not valid:
            return render_template("activities/create.html", msg="Invalid creation!")
        if valid:
            activity.create_activity(**data)
            return render_template("activities/create.html", msg="Success!")
    return render_template("activities/create.html")

@app.route('/activities/delete', methods = ["POST"])
def delete_activity():
    id = request.args.get('id', None)
    if id is not None:
        id = int(id)
        activity.delete_activity(id)

    return redirect("/activities")

@app.route('/activities/update', methods = ["GET", "POST"])
def update_activity():
    if request.method == "POST":
        task_name = request.form["task_name"]
        category = request.form["category"]
        hours = int(request.form["hours"])
        query = """
    UPDATE "activity"
    SET "hours" = ?,
    category = ?
    WHERE assignment_id = ?;
    """
        params = [hours, category, task_name]
        try:
            conn = sqlite3.connect("capstone.db")
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            print(f'Database error: {e}')
        finally:
            conn.close()

        msg = ["Successful", task_name, category, hours]
        return render_template('activities/edit.html', msg = msg) 
    return render_template("activities/edit.html")