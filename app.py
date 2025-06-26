from flask import Flask, render_template
from datetime import timedelta
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os
from extensions import oauth
from routes.landing_page import landing_page_bp
from routes.auth_routes import auth_bp
from routes.dashboard import dashboard_bp
from routes.my_courses import my_courses_bp
from errors.handlers import errors
from routes.ai_chat import ai_chat_bp
from routes.compiler import compiler_bp


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("app_secret_key")
app.permanent_session_lifetime = timedelta(days=1)

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

if __name__ == "__main__":
    app.run(debug=True)
