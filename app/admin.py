from flask import Blueprint, render_template
from models import School, User, Subject
from forms import DeleteForm
from auth import login_required

bp = Blueprint("admin", __name__)

@bp.route("/admin")
@login_required
def index():
    form = DeleteForm()
    users = User().query.all()
    subjects = Subject().query.all()
    schools = School().query.all()

    if form.validate_on_submit():
        return render_template("admin.html", form=form)
    return render_template("admin.html", users=users, subjects=subjects, schools=schools, form=form )
