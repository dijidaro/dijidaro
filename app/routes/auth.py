from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/registration", methods=["GET", "POST"])
def register_user():
    return render_template("pages/auth/register.html")

@auth_bp.route("/user_login", methods=["GET", "POST"])
def login_user():
    return render_template("pages/auth/login.html")