from flask import Blueprint, render_template

bp = Blueprint("about", __name__)

@bp.route("/about", methods=["GET"])
def about_us():
    return render_template("about.html")
