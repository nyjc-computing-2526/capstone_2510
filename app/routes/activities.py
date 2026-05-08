from flask import Flask, request
from services.render import render_template
from app_obj import app
import sqlite3

@app.route('/activities')
def activities():
    return render_template("activities/activities.html", activities=activities)

def valid_create(task_name, hours):
    if type(task_name) != str() or task_name == "":
        return False
    #category will be a dropdown box, no way to get error
    if type(hours) != float or hours <= 0:
        return False
    return True

@app.route('/activities/create', methods = ["GET", "POST"])
def create_activity():
    if request.method == "POST":
        task_name = request.form["task_name"]
        category = request.form["category"]
        hours = int(request.form["hours"])
        valid = valid_create(task_name, hours)
        if valid:
            query = """INSERT INTO activity (task_name, category, hours)
            VALUES (?, ?, ?)"""
            params = [task_name, category, hours]
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
    return render_template("activities/create.html")

@app.route('/activities/delete', methods = ["POST"])
def delete_activity():
    query = "DELETE FROM activity WHERE task_name = ?;"
    task_name = request.form["task_name"]
    params = [task_name]
    try:
        conn = sqlite3.connect("capstone.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f'Database error: {e}')
    finally:
        conn.close()

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