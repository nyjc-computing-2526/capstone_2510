
from flask import Flask, request, redirect, session, url_for
from services.render import render_template
from services.auth_service import create_user, email_exists, get_user, check_pw
from app_obj import app

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        password_again = request.form["password_again"]

        if password != password_again:
            return render_template("register.html", msg="Passwords do not match!")

        if email_exists(email):
            return render_template("register.html", msg="Email already exists!")

        create_user(name, email, password)
        return redirect(url_for("login", msg="Registration successful. Please log in"))
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
        if not check_pw(user["password"], password):
            return render_template("login.html", msg="Wrong Password!")

        #store session
        session["name"] = user["name"]
        session["email"] = user["email"]
        session["logged_in"] = True

        return redirect("/activities")

    return render_template("login.html", msg = request.args.get('msg', None))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

