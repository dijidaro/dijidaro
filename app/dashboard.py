from flask import Blueprint, render_template
from models import Student
from forms import DeleteForm

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index():
    form = DeleteForm()
    students = Student().query.all()
    print(students)
    print("Hello world")
    return render_template("index.html", students=students, form=form)
