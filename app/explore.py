from flask import Blueprint, render_template

bp = Blueprint("explore", __name__)

@bp.route("/explore", methods=["GET"])
def explore_resources():
    return render_template("explore.html")