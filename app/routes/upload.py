from flask import Blueprint, render_template, redirect, url_for
from routes.auth import login_required
from forms import UploadResourceForm

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resource():
    form = UploadResourceForm()
    if form.validate_on_submit():
        error = None
        return redirect(url_for("explore.explore_resources"))
    return render_template("pages/upload.html", form=form)
