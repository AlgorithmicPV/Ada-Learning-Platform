from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("user_id"):
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        user_id = session.get("user_id")
        cursor.execute(
            "SELECT full_name FROM User WHERE user_id=?", (user_id,))
        username = cursor.fetchone()[0]
        return render_template("user/dashboard.html",
                               username=username)
    else:
        return redirect(url_for("auth.login"))
