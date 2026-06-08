from flask import Blueprint, redirect, render_template, request, url_for

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("login.html")
