from flask import Blueprint, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError
from models import Student, db
from forms import StudentRegistrationForm, StudentLoginForm
from werkzeug.security import generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/student_registration", methods=("GET", "POST"))
def register_student():
    form = StudentRegistrationForm()

    if form.validate_on_submit():
        try:
            student = Student(first_name=form.firstname.data, last_name=form.lastname.data, username=form.username.data, email=form.email.data, 
                              gender=form.gender.data, birth_date=form.birthdate.data, password=generate_password_hash(form.password.data) )
            db.session.add(student)
            db.session.commit()
        except IntegrityError as e:
            error = f"Request failed! You either entered an already existing username and/or email. {e}"
            db.session.rollback()
            print(error)
        else:
            return redirect(url_for("auth.login_student"))
        
    return render_template("auth/register.html", form=form)

@bp.route("student_login", methods=("GET", "POST"))
def login_student():
    form = StudentLoginForm()
    return render_template("auth/login.html", form=form)

@bp.route("/delete/<int:student_id>", methods=("POST"))
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("auth.login_student"))