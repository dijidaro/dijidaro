import functools
from flask import Blueprint, flash, redirect, render_template, session, url_for, g
from forms import UserRegistrationForm, UserLoginForm
import re
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/registration", methods=["GET", "POST"])
def register_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        error = None
        if not validate_username(form.username.data.lower()):
            error = "Invalid username."
        if not validate_password(form.password.data):
            error = "Password must be at least 8 characters long, contains at least one uppercase letter, one lowercase letter, and one number."
            if not form.password.data == form.password2.data:
                error = "Passwords must match"
        
        if error is None:
            try:
                user = User(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, 
                            birth_date=form.birth_date.data, user_type=form.user_type.data, email=form.email.data, 
                            username=form.username.data, password=generate_password_hash(form.password.data))
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                error = "Request failed! You either entered an already existing username and/or email"
                db.session.rollback()
                flash(error)
                print(e)
            else:
                return redirect(url_for("auth.login_user"))
        flash(error)
    return render_template("pages/auth/register.html", form=form)

@auth_bp.route("/user_login", methods=["GET", "POST"])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        error = None
        errorMessage = "The information you entered does not match our records for accessing this service. You either entered an invalid email and/or password or you do not have privilege to access this service. Please try to enter your email and password again!"
        user = User.query.filter_by(username=form.username.data).all()
        print(user)
        if not user:
            error = errorMessage

        for row in user:
            if not check_password_hash(row.password, form.password.data):
                error = errorMessage
            if error is None:
                session.clear()
                session["user_id"] = row.id
                flash(f"Logged in as {row.username}")
                return redirect(url_for("home.index"))
            flash(error)
    return render_template("pages/auth/login.html", form=form)

# Log user out
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))

@auth_bp.before_app_request
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
    # return False

def validate_password(password):
    """ Validates the password using the provided regular 
    expression i.e `pattern`. Returns `True` if password 
    matches the pattern and `False` otherwise. """
    pattern = r"^(?=.*[!@#$%^&*(),.?':{}|<>])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*(),.?':{}|<>]{8,}$"
    if re.match(pattern, password):
        return True
    return False