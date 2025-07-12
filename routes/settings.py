from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import sqlite3
import uuid
from datetime import datetime, date
import markdown

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings")
def settings():
    if "user_id" in session:
        return render_template("user/settings.html")
    else:
        return redirect(url_for("auth.login"))