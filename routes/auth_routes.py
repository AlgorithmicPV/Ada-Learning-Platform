from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session,
    current_app,
)
import os
from datetime import datetime, timedelta
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from dotenv import load_dotenv
from extensions import oauth
from utils import validate_email_address, db_execute

load_dotenv()

auth_bp = Blueprint("auth", __name__)  # Blueprint for authentication routes
auth_bp.permanent_session_lifetime = timedelta(
    days=1)  # Set session lifetime to 1 day

ph = PasswordHasher()  # Password hasher for secure password storage

# Initialize OAuth for Google login
google = oauth.register(
    "Ada",
    client_id=os.getenv("Client_ID"),
    client_secret=os.getenv("Client_secret"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account"})

# Route for the Normal Login


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.args.get('next'):
        next_url = request.args.get('next')
    else:
        next_url = url_for("dashboard.dashboard")
    session.clear()
    if (
        request.method == "POST"
    ):  # If the request method is POST, it means the user is trying to log in
        email = request.form.get("email")
        password = request.form.get("password")

        # Validates the email and password fields are not empty
        # If they contain only empty spaces it will return a flash message
        # saying that "Email and password required"
        if email != "" and not email.isspace() and password != "" and not password.isspace():
            password_query = "SELECT password FROM User WHERE email = ?"
            # Fetch the stored password hash for the given email
            # stored_hash_password is a tuple, so we need to access the first
            # element
            stored_hash_password = db_execute(
                query=password_query,
                fetch=True,
                fetchone=True,
                values=(email,)
            )

            if stored_hash_password:
                try:
                    if ph.verify(
                            stored_hash_password[0],
                            password):  # Verify the password
                        session["email"] = email
                        user_info_query = """
                                        SELECT
                                            full_name,
                                            user_id
                                        FROM User
                                        Where email = ?"""
                        user_info = db_execute(
                            query=user_info_query,
                            fetch=True,
                            fetchone=False,
                            values=(email,))
                        username = user_info[0][0]
                        # Store the username in the session
                        session["username"] = username
                        user_id = user_info[0][1]
                        # Store the user_id in the session
                        session["user_id"] = user_id
                        session["auth_provider"] = "manual"
                        return redirect(next_url)
                except (
                    VerifyMismatchError
                ):  # If the password does not match the stored hash
                    flash("Password is not correct", category="error")
                    return redirect(url_for("auth.login"))
                except InvalidHash:  # If the password hash is invalid
                    flash(
                        "Invalid hash format. The hash may be corrupted",
                        category="error")
                    return redirect(url_for("auth.login"))
                except Exception as e:  # Catch any other exceptions
                    flash(f"An error occured: {e}", category="error")
                    return redirect(url_for("auth.login"))
            else:  # If the email does not exist in the database
                flash("User does not exist", category="error")
        else:
            flash("Email and password required", category="error")

    return render_template("auth/login.html")


# Create an account page
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        email_query = "SELECT email FROM User WHERE email = ?"
        existing_email = db_execute(query=email_query,
                                    fetch=True,
                                    fetchone=True,
                                    values=(email, )
                                    )

        if not email or not name or not password or not confirm_password:
            flash("All fields are required!", category="error")

        elif existing_email:
            flash("Email is already in use.", category="error")

        elif password != confirm_password:
            flash("Passwords don't match!", category="error")

        elif len(name) < 2:
            flash("Username is too short.", category="error")

        elif len(password) < 6:
            flash("Password is too short.", category="error")

        elif validate_email_address(email) == "invalid":
            flash("Invalid email!", category="error")

        else:

            user_id = str(uuid.uuid4())  # Creates a new primary key

            # Creates a random image ID for DiceBear to generate an avatar
            # for the user
            image_id = str(uuid.uuid4())

            timestamp = datetime.now().isoformat(
                timespec="seconds"
            )  # Gets the current time

            insert_query = """
                INSERT
                INTO User
                    (user_id,
                    email,
                    full_name,
                    password,
                    auth_provider,
                    theme_preference,
                    join_date,
                    profile_image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

            db_execute(query=insert_query,
                       fetch=False,
                       values=(user_id,
                               email,
                               name,
                               ph.hash(password),
                               "manual",
                               "dark",
                               datetime.fromisoformat(timestamp),
                               f"https://api.dicebear.com/9.x/identicon/svg?seed={
                                   image_id}",
                               )
                       )

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

    userToken = session.get("user")
    userInfo = userToken["userinfo"]
    username = userInfo["given_name"]
    email = userInfo["email"]
    profile_pic = userInfo["picture"]
    google_id = userInfo["sub"]

    user_id = str(uuid.uuid4())  # Creates a new primary key

    timestamp = datetime.now().isoformat(
        timespec="seconds")  # Gets the current time
    print("Session state (login):", session.get('oauth_state'))

    insert_query = """
        INSERT
        INTO User
            (user_id,
            email,
            full_name,
            google_id,
            auth_provider,
            profile_image,
            theme_preference,
            join_date)
        SELECT ?, ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM User WHERE email = ?
            )"""

    db_execute(query=insert_query,
               fetch=False,
               values=(user_id,
                       email,
                       username,
                       google_id,
                       "google",
                       profile_pic,
                       "dark",
                       timestamp,
                       email))

    session["username"] = username
    email_query = "SELECT user_id FROM User Where email = ?"
    # Fetch the user_id associated with the email
    stored_user_id = db_execute(query=email_query,
                                fetch=True,
                                fetchone=True,
                                values=(email,))
    user_id = stored_user_id[0]
    session["user_id"] = user_id  # Store the user_id in the session
    session["auth_provider"] = "google"

    return redirect(url_for("dashboard.dashboard"))
