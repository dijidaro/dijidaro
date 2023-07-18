import re
from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from models import Student, db
from forms import StudentRegistrationForm, StudentLoginForm
from werkzeug.security import generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

def validate_username(username):
    pattern = r"[a-z0-9_]{5,20}$"
    if re.match(pattern, username):
        return True
    return False

def validate_password(password):
    pattern = r"^(?=.*[!@#$%^&*(),.?':{}|<>])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*(),.?':{}|<>]{8,}$"
    if re.match(pattern, password):
        return True
    return False

@bp.route("/student_registration", methods=("GET", "POST"))
def register_student():
    form = StudentRegistrationForm()

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
                student = Student(first_name=form.firstname.data, last_name=form.lastname.data, username=form.username.data, email=form.email.data, 
                                gender=form.gender.data, birth_date=form.birthdate.data, password=generate_password_hash(form.password.data) )
                db.session.add(student)
                db.session.commit()

            except IntegrityError as e:
                error = f"Request failed! You either entered an already existing username and/or email. {e}"
                db.session.rollback()
                flash(error)
                print(error)
                
            else:
                return redirect(url_for("auth.login_student"))
        
        flash(error)

    return render_template("auth/register.html", form=form)


@bp.route("student_login", methods=("GET", "POST"))
def login_student():
    form = StudentLoginForm()
    return render_template("auth/login.html", form=form)


@bp.route("/delete/<int:student_id>", methods=("POST", "GET"))
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("auth.login_student"))