from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("username"):
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        user_id = session.get("user_id")
        return render_template("user/dashboard.html", username=session["username"])
    else:
        return redirect(url_for("auth.login"))
