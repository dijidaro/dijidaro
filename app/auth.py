import functools
import re
from flask import Blueprint, render_template, redirect, url_for, flash, session, g
from sqlalchemy.exc import IntegrityError
from models import User, db
from forms import UserRegistrationForm, UserLoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/registration", methods=("GET", "POST"))
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        error = None
        if not validate_username(form.username.data.lower()):
            error = "Invalid username."
        if not validate_password(form.password.data):
            error = "Password must be at least 8 characters long, contains at least one uppercase letter, one lowercase letter, and one number."
            if not form.password.data == form.password2.data:
                error = "Passwords must match."

        if error is None:
            try:
                user = User( first_name=form.firstname.data, last_name=form.lastname.data, 
                                username=form.username.data, user_type=form.usertype.data, 
                                email=form.email.data, gender=form.gender.data, 
                                birth_date=form.birthdate.data, password=generate_password_hash(form.password.data) )
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                error = "Request failed! You either entered an already existing username and/or email"
                db.session.rollback()
                flash(error)
                print(e)
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html", form=form)

@bp.route("user_login", methods=("GET", "POST"))
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        error = None
        errorMessage = "The information you entered does not match our records for accessing this service. You either entered an invalid email and/or password or you do not have privilege to access this service. Please try to enter your email and password again!"
        user = User.query.filter_by(username=form.username.data).all()
        if not user:
            error = errorMessage
        
        # Check if passwords match.
        for row in user:
            if not check_password_hash(row.password, form.password.data):
                error = errorMessage
        if error is None:
            session.clear()
            session["user_id"] = row.id
            flash("Logged in successfully")
            return redirect(url_for("dashboard.index"))
        flash(error)
    return render_template("auth/login.html", form=form)

# Log out a user
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard.index"))

@bp.route("/delete/<int:user_id>", methods=("POST", "GET"))
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("auth.login"))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# Require athentication in other views.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


# HELPER FUNCTIONS

def validate_username(username):
    """ Ensures min/max number of characters.Checks that username doesn't 
    begin with numbers and no special characters. Returns `True` if the 
    username matches the pattern and `False` otherwise.
    """
    pattern = r"[a-z0-9_]{5,20}$"
    if re.match(pattern, username):
        return True
    return False

def validate_password(password):
    """ Validates the password using the provided regular 
    expression i.e `pattern`. Returns `True` if password 
    matches the pattern and `False` otherwise. """
    pattern = r"^(?=.*[!@#$%^&*(),.?':{}|<>])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*(),.?':{}|<>]{8,}$"
    if re.match(pattern, password):
        return True
    return False
