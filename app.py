"""
Main app.py
"""

import os
import sqlite3
from datetime import timedelta

from flask import Flask, session, redirect, url_for, request
from flask.sessions import SecureCookieSessionInterface
from werkzeug.middleware.proxy_fix import ProxyFix
from argon2 import PasswordHasher
from dotenv import load_dotenv

from extensions import oauth
from errors.handlers import errors
from routes.ai_chat import ai_chat_bp
from routes.auth_routes import auth_bp
from routes.community import community_bp
from routes.compiler import compiler_bp
from routes.dashboard import dashboard_bp
from routes.landing_page import landing_page_bp
from routes.my_courses import my_courses_bp
from routes.practice_hub import practice_hub_bp
from routes.settings import settings_bp


load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config['PREFERRED_URL_SCHEME'] = 'https'

app.secret_key = os.getenv("app_secret_key")
app.permanent_session_lifetime = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path, 'static', 'images', 'profile_pics')
ph = PasswordHasher()

oauth.init_app(app)

# Landing Page
app.register_blueprint(landing_page_bp)

# login page
app.register_blueprint(auth_bp)

# Dashboard of the application
app.register_blueprint(dashboard_bp)

# My Courses section
app.register_blueprint(my_courses_bp)

# Ai chat
app.register_blueprint(ai_chat_bp)

# Compiler
app.register_blueprint(compiler_bp)

# Community section
app.register_blueprint(community_bp)

# Practice hub section
app.register_blueprint(practice_hub_bp)

# Settings Page
app.register_blueprint(settings_bp)

# Error section
app.register_blueprint(errors)


@app.context_processor
def inject_user_info():
    """
    This context processor injects the user's profile image into all
    templates.

    The function checks if a user_id exists in the session. If it does,
    it queries the database for the user's profile image. Depending on
    whether the image path is remote (URL) or local (static folder), it
    sets the image_source in the session. It then returns a dictionary
    with the profile_pic and image_source for use in templates. If no
    user is logged in, a default profile picture is returned.


    Returns:
        - dict: A dictionary with profile_pic and image_source for Jinja2
        templates.
    """
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        user_id = session.get("user_id")

        cursor.execute(
            "SELECT profile_image FROM User WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        # auth_provider = session.get("auth_provider")
        if result and result[0]:
            profile_pic = result[0]
            if profile_pic.startswith("https"):
                image_source = "remote"
                session['image_source'] = image_source
            else:
                image_source = "local"
                session['image_source'] = image_source
            return dict(profile_pic=profile_pic, image_source=image_source)
    return dict(profile_pic="images/profile_pics/default-pic.png")


@app.route("/logout")
def logout():
    """
    This route logs out the user and clears the session.

    The function checks if "user_id" is in the session. If yes, it clears
    the session and redirects the user to the landing page. If not, it
    redirects the user to the login page.


    Returns:
        - Redirect to the landing page or login page.
    """
    if "user_id" in session:
        session.clear()
        return redirect(url_for("landing_page.landing_page"))
    else:
        return redirect(url_for("auth.login"))


@app.after_request
def calculate_session_size(response):
    """
    This after-request function logs the size of the user's session.

    The function creates a SecureCookieSessionInterface and uses its
    serializer to encode the current session. It then calculates the
    size in bytes and prints it with the request path. Finally, it
    returns the original response unchanged.

    Args:
        response (Response): The response object from the route.

    Returns:
        Response: The same response object, passed back unchanged.
    """
    interface = SecureCookieSessionInterface()
    serializer = interface.get_signing_serializer(app)

    if serializer:
        encoded = serializer.dumps(dict(session))
        size_bytes = len(encoded.encode('utf-8'))
        print(f"Session size for {request.path}: {size_bytes} bytes")

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
