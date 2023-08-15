from flask import Blueprint, render_template
from models import User
from forms import DeleteForm

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index():
    form = DeleteForm()
    users = User().query.all()

    if form.validate_on_submit():
        return render_template("index.html", form=form)
    return render_template("index.html", users=users, form=form )
