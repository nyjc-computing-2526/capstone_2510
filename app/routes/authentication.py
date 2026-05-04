
from flask import Flask, request, render_template, redirect, session
from services.auth_service import create_user, email_exists, get_user
from app_obj import app

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email_exists(email):
            return render_template("register.html", msg="Email already exists!")

        create_user(email, password)
        return redirect("/login", msg="Registration successful. Please log in")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email)

        # check if user exists
        if user is None:
            return render_template("login.html", msg="User does not exist!")

        # check password
        if user["password"] != password:
            return render_template("login.html", msg="Wrong Password!")

        #store session
        session["user_id"] = user["id"]
        session["email"] = user["email"]

        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.context_processor
def inject_user():
    return dict(logged_in=session.get("user_id") is not None)

