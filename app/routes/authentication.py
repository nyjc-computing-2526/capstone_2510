
from flask import Blueprint, request
from app.services.auth_service import create_user, email_exists, get_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]


        if email_exists(email):
            return "Email already exists"

        create_user(email, password)
        return redirect("/login")
    else:
        return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email)

        # check if user exists
        if user is None:
            return render_template("login.html", msg="User does not exist")

        # check password
        if user["password"] != password:
            return render_template("login.html", msg="Wrong Password")

        #store session
        session["user_id"] = user["id"]
        session["email"] = user["email"]

        return redirect("/")

    return render_template("login.html")
