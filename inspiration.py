@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy-policy")
def privacy():
    return render_template("legal.html")

from flask import request, redirect, session, url_for

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db_execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        if user:
            session["user_id"] = user[0][0]  # assuming id is first column
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db_execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/activities")
def activities():
    data = db_execute("SELECT * FROM activities")
    return render_template("activitylist.html", activities=data)

@app.route("/activities/myactivities")
def my_activities():
    user_id = session.get("user_id")

    created = db_execute(
        "SELECT * FROM activities WHERE creator_id = ?",
        (user_id,)
    )

    joined = db_execute(
        """
        SELECT a.* FROM activities a
        JOIN participants p ON a.id = p.activity_id
        WHERE p.user_id = ?
        """,
        (user_id,)
    )

    return render_template(
        "ownactivity.html",
        created=created,
        joined=joined
    )

@app.route("/activities/create", methods=["GET", "POST"])
def create_activity():
    if request.method == "POST":
        name = request.form.get("name")
        user_id = session.get("user_id")

        db_execute(
            "INSERT INTO activities (name, creator_id) VALUES (?, ?)",
            (name, user_id)
        )

        return redirect(url_for("activities"))

    return render_template("createactivity.html")

@app.route("/activities/update/<int:id>", methods=["GET", "POST"])
def update_activity(id):
    if request.method == "POST":
        name = request.form.get("name")

        db_execute(
            "UPDATE activities SET name = ? WHERE id = ?",
            (name, id)
        )

        return redirect(url_for("activities"))

    activity = db_execute(
        "SELECT * FROM activities WHERE id = ?",
        (id,)
    )

    return render_template("updateactivity.html", activity=activity)

@app.route("/activities/delete/<int:id>", methods=["POST"])
def delete_activity(id):
    user_id = session.get("user_id")

    db_execute(
        "DELETE FROM activities WHERE id = ? AND creator_id = ?",
        (id, user_id)
    )

    return redirect(url_for("activities"))

@app.route("/activities/join/<int:id>", methods=["GET", "POST"])
def join_activity(id):
    user_id = session.get("user_id")

    if request.method == "POST":
        db_execute(
            "INSERT INTO participants (user_id, activity_id) VALUES (?, ?)",
            (user_id, id)
        )
        return redirect(url_for("activities"))

    return render_template("joinactivity.html", activity_id=id)

@app.route("/activities/leave/<int:id>", methods=["POST"])
def leave_activity(id):
    user_id = session.get("user_id")

    db_execute(
        "DELETE FROM participants WHERE user_id = ? AND activity_id = ?",
        (user_id, id)
    )

    return redirect(url_for("activities"))
