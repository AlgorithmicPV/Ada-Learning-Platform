from flask import (
    Blueprint,
    render_template,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session,
    current_app,
)
import os
import sqlite3
from datetime import datetime, timedelta
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from extensions import oauth

load_dotenv()

auth_bp = Blueprint("auth", __name__)  # Blueprint for authentication routes
auth_bp.permanent_session_lifetime = timedelta(days=1)  # Set session lifetime to 1 day

ph = PasswordHasher()  # Password hasher for secure password storage

# Initialize OAuth for Google login
google = oauth.register(
    "Ada",
    client_id=os.getenv("Client_ID"),
    client_secret=os.getenv("Client_secret"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
    ):  # If the request method is POST, it means the user is trying to log in
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM User WHERE email = ?", (email,)
        )  # Fetch the stored password hash for the given email
        stored_hash_password = (
            cursor.fetchone()
        )  # stored_hash_password is a tuple, so we need to access the first element

        if stored_hash_password:
            try:
                if ph.verify(stored_hash_password[0], password):  # Verify the password
                    session["email"] = email
                    conn = sqlite3.connect("database/app.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT full_name FROM User Where email = ?", (email,)
                    )  # Fetch the username associated with the email
                    stored_username = (
                        cursor.fetchone()
                    )  # stored_username is a tuple, so we need to access the first element
                    username = stored_username[0]
                    session["username"] = username  # Store the username in the session
                    cursor.execute(
                        "SELECT user_id FROM User Where email = ?", (email,)
                    )  # Fetch the user_id associated with the email
                    stored_user_id = cursor.fetchone()
                    user_id = stored_user_id[0]
                    session["user_id"] = user_id  # Store the user_id in the session
                    cursor.close()  # Close the database connection
                    return redirect(url_for("dashboard.dashboard"))
            except (
                VerifyMismatchError
            ):  # If the password does not match the stored hash
                flash("Password is not correct", category="error")
                return redirect(url_for("auth.login"))
            except InvalidHash:  # If the password hash is invalid
                flash(
                    "Invalid hash format. The hash may be corrupted", category="error"
                )
                return redirect(url_for("auth.login"))
            except Exception as e:  # Catch any other exceptions
                flash(f"An error occured: {e}", category="error")
                return redirect(url_for("auth.login"))
        else:  # If the email does not exist in the database
            flash("Username doesn't exist", category="error")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


# Create an account page
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        cursor.execute("SELECT email FROM User")
        email_list = cursor.fetchall()

        saved_emails = []  # An array to collect all the emails from the database

        # Converts the email list into a flat array to easily check if the entered email is valid or not. email_list is a list of 1-element tuples
        for email_tuple in email_list:
            for email_from_db in email_tuple:
                saved_emails.append(email_from_db)

        cursor.execute("SELECT full_name FROM User")
        full_name_list = cursor.fetchall()

        saved_names = []  # An array to collect all the names from the database

        # Converts the full_name_list into a flat array to easily check if the entered name is valid or not. full_name_list is a list of 1-element tuples
        for name_tuple in full_name_list:
            for name_from_db in name_tuple:
                saved_names.append(name_from_db)

        conn.close()

        if not email or not name or not password or not confirm_password:
            flash("All fields are required!", category="error")

        elif email in saved_emails:
            flash("Email is already in use.", category="error")

        elif name in saved_names:
            flash("Username is already in use.", category="error")

        elif password != confirm_password:
            flash("Passwords don't match!", category="error")

        elif len(name) < 2:
            flash("Username is too short.", category="error")

        elif len(password) < 6:
            flash("Password is too short.", category="error")

        elif "@" not in email:
            flash("Invalid email!", category="error")

        else:

            user_id = str(uuid.uuid4())  # Creates a new primary key

            timestamp = datetime.now().isoformat(
                timespec="seconds"
            )  # Gets the current time

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO User (user_id, email, full_name, password, auth_provider, theme_preference, join_date) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    user_id,
                    email,
                    name,
                    ph.hash(password),
                    "manual",
                    "dark",
                    datetime.fromisoformat(timestamp),
                ),
            )

            conn.commit()
            cursor.close()

            return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


# login for google
@auth_bp.route("/login/google")
def login_google():
    try:
        redirect_uri = url_for("auth.authorize_google", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        current_app.logger.error(f"Error during the logon: {str(e)}")
        return "Error occured during login", 500


@auth_bp.route("/authorize/google")
def authorize_google():
    token = google.authorize_access_token()
    session["user"] = token
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()

    userToken = session.get("user")
    userInfo = userToken["userinfo"]
    username = userInfo["given_name"]
    email = userInfo["email"]
    cursor.execute("SELECT email FROM User")
    email_list = cursor.fetchall()

    saved_emails = []  # An array to collect all the emails from the database

    # # Converts the email list into a flat array to easily check if the entered email is valid or not. email_list is a list of 1-element tuples
    for email_tuple in email_list:
        for email_from_db in email_tuple:
            saved_emails.append(email_from_db)

    user_id = str(uuid.uuid4())  # Creates a new primary key

    timestamp = datetime.now().isoformat(timespec="seconds")  # Gets the current time

    if email not in saved_emails:
        cursor.execute(
            """INSERT INTO User (user_id, email, full_name, auth_provider, theme_preference, join_date) VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, email, username, "google", "dark", timestamp),
        )

        conn.commit()

    session["username"] = username
    cursor.execute(
        "SELECT user_id FROM User Where email = ?", (email,)
    )  # Fetch the user_id associated with the email
    stored_user_id = cursor.fetchone()
    user_id = stored_user_id[0]
    session["user_id"] = user_id  # Store the user_id in the session
    cursor.close()  # Close the database connection

    return redirect(url_for("dashboard.dashboard"))
