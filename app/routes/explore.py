from flask import Blueprint, render_template

explore_bp = Blueprint("explore", __name__)

@explore_bp.route("/explore", methods=["GET"])
def explore_resources():
    return render_template("pages/explore.html")
