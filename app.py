from flask import Flask, render_template, session, redirect, url_for
from datetime import timedelta
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os
import sqlite3
from extensions import oauth
from routes.landing_page import landing_page_bp
from routes.auth_routes import auth_bp
from routes.dashboard import dashboard_bp
from routes.my_courses import my_courses_bp
from errors.handlers import errors
from routes.ai_chat import ai_chat_bp
from routes.compiler import compiler_bp
from routes.community import community_bp
from routes.practice_hub import practice_hub_bp
from routes.settings  import settings_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("app_secret_key")
app.permanent_session_lifetime = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images' ,'profile_pics')
ph = PasswordHasher()

oauth.init_app(app)

# Landing Page
app.register_blueprint(landing_page_bp)

# login page
app.register_blueprint(auth_bp)

# Dashboard of the application
app.register_blueprint(dashboard_bp)

# My Courses Page
app.register_blueprint(my_courses_bp)

app.register_blueprint(errors)

app.register_blueprint(ai_chat_bp)

app.register_blueprint(compiler_bp)

app.register_blueprint(community_bp)

app.register_blueprint(practice_hub_bp)

app.register_blueprint(settings_bp)

@app.context_processor
def inject_user_info():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        user_id = session.get("user_id")

        cursor.execute(
            "SELECT profile_image FROM User WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        auth_provider = session.get("auth_provider")
        if result and result[0]:
            profile_pic = result[0]
            return dict(profile_pic=profile_pic, auth_provider = auth_provider)
    return dict(profile_pic="images/profile_pics/default-pic.png")

@app.route("/logout")
def logout():
    if "user_id" in session:
        session.clear()
        return redirect(url_for("landing_page.landing_page"))
    else:
        return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)

