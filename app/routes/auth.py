import functools
from flask import Blueprint, flash, redirect, render_template, session, url_for, g
from app.forms import UserRegistrationForm, UserLoginForm
import re
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Constants for validation messages
INVALID_USERNAME = "Invalid username. It must be 5-20 characters long, contain only letters, numbers, and underscores."
INVALID_PASSWORD = "Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, one number, and one special character."
PASSWORDS_MISMATCH = "Passwords must match."
DUPLICATE_USER = "Username or email already exists."
LOGIN_ERROR = "Invalid username or password."

@auth_bp.route("/registration", methods=["GET", "POST"])
def register_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        error = None
        if not validate_username(form.username.data.lower()):
            error = INVALID_USERNAME
        if not validate_password(form.password.data):
            error = INVALID_PASSWORD
            if form.password.data != form.password2.data:
                error = PASSWORDS_MISMATCH
        
        if error is None:
            try:
                user = User(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, 
                            birth_date=form.birth_date.data, user_type=form.user_type.data, email=form.email.data, 
                            username=form.username.data, password=generate_password_hash(form.password.data))
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                error = DUPLICATE_USER
                db.session.rollback()
                flash(error)
                print(e)
            else:
                flash("Registration successful! Please log in.")
                return redirect(url_for("auth.login_user"))
        
        flash(error)

    return render_template("pages/auth/register.html", form=form)

@auth_bp.route("/user_login", methods=["GET", "POST"])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if not user or not check_password_hash(user.password, form.password.data):
            error = LOGIN_ERROR

        if error is None:
            session.clear()
            session["user_id"] = user.id
            flash(f"Logged in as {user.username}")
            return redirect(url_for("home.index"))
        
        flash(error)
    
    return render_template("pages/auth/login.html", form=form)

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# Log user out
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))


@auth_bp.route("/delete/<int:user_id>", methods=("POST", "GET"))
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("auth.login_user"))


# Require athentication in other views.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_user"))
        return view(**kwargs)
    return wrapped_view




# HELPER FUNCTIONS
def validate_username(username):
    """ Ensures min/max number of characters.Checks that username doesn't 
    begin with numbers and no special characters. Returns `True` if the 
    username matches the pattern and `False` otherwise.
    """
    pattern = r"[a-z0-9_]{5,20}$"
    return bool(re.match(pattern, username))

def validate_password(password):
    """ Validates the password using the provided regular 
    expression i.e `pattern`. Returns `True` if password 
    matches the pattern and `False` otherwise. """
    pattern = r"^(?=.*[!@#$%^&*(),.?':{}|<>])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*(),.?':{}|<>]{8,}$"
    if re.match(pattern, password):
        return True
    return False