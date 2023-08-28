from flask import Blueprint, render_template
from forms import UploadForm

bp = Blueprint("upload", __name__)

@bp.route("/upload")
def upload_resource():
    form = UploadForm()
    return render_template("upload.html", form=form)


