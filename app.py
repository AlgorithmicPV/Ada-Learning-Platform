from flask import Flask, render_template
from datetime import timedelta
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os
from routes.landing_page import landing_page_bp
from routes.auth_routes import auth_bp
from extensions import oauth

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
@app.route("/dashboard")
def dashboard():
    # if "username" in session:
    #     return render_template("dashboard.html", username=session["username"])
    # return redirect(url_for('login'))
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)