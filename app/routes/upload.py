from flask import Blueprint, render_template
from routes.auth import login_required

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["GET"])
@login_required
def upload_resource():
    return render_template("pages/upload.html")
