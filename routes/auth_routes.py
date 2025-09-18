"""
Handles all the authentications of the system
"""

import os
from datetime import datetime, timedelta
import uuid
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
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from dotenv import load_dotenv
from extensions import oauth
from utils import validate_email_address, db_execute

load_dotenv()

auth_bp = Blueprint("auth", __name__)  # Blueprint for authentication routes
auth_bp.permanent_session_lifetime = timedelta(
    days=1)  # Set session lifetime to 1 day, for the users' security

ph = PasswordHasher()  # Password hasher for secure password storage

# Initialize OAuth for Google login
google = oauth.register(
    "Ada",
    client_id=os.getenv("Client_ID"),
    client_secret=os.getenv("Client_secret"),
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"),
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account"})


# Route for the Normal Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    This route does the normal login (not for Google logins),
    and also render login.html.

    This route clears all the previous session data.
    Gets the hashed password from the database
    according to the typed user email,
    and checks that with the typed hashed password. If the login is successful,
    It gets the full name, user ID, and auth provider from the database,
    and saves that information in session storage for future usage.
    Then redirect to the dashboard.

    Returns:
        - Initially, it renders the login.html
        - If the login is successful, it redirects to the dashboard
        - If the passwords do not match,
          it sends a flash message called "Password is not correct".
        - If the password hash is invalid,
          it sends a flash message called "Invalid hash format.
          The hash may be corrupted".
        - For the exception,
          It sends the flash message with the relevant error.
    """
    session.clear()
    if (
        request.method == "POST"
    ):  # If the request method is POST, it means the user is trying to log in
        email = request.form.get("email")
        password = request.form.get("password")

        # Validates the email and password fields are not empty
        # If they contain only empty spaces it will return a flash message
        # saying that "Email and password required"
        if (email.strip() != "" and
                password.strip() != ""):
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
                        return redirect(url_for("dashboard.dashboard"))
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
    """
    This route does the sign-up. It clears previous session data for security.
    It renders the signup.html.

    Gets the email, name, and passwords
    (including both passwords and confirmation passwords).
    Before the signup process,
        check that the typed email exists in the database.
    If the signing is successful, it redirects to the login route.
    Use the' validate_email_address' function
        to validate the user's email address.
    Use the uuid4 to generate a unique ID.
    Use the dicebear API to generate a custom profile image,
    and for that, also use a UUID4 code.
    (Not using the userID, as other users can see that ID,
    through the profile image link,
    when they open another user's image on the web separately)

    Return:
        - Initially, it renders "signup.html".
        - If the email is already in the database,
          it says "Email is already in use.".
        - If the inputs are empty, it says "All fields are required!"
        - If the passwords do not match, it says "Passwords don't match!"
        - If the display name is less than 3, it says "Username is too short."
        - If the password is less than 6, it says "Password is too short."
        - If the display name is more than 50 characters,
          it says "Display name is too long. Maximum allowed is 50 characters."
        - If the password is more than 1024 characters,
          it says "Password is too long. Maximum allowed is 1,024 characters."
        - If the user typed email is not valid, it says "Invalid email!"

    *All the messages are done by flash messages
    """
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        display_name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        email_query = "SELECT email FROM User WHERE email = ?"
        existing_email = db_execute(query=email_query,
                                    fetch=True,
                                    fetchone=True,
                                    values=(email, )
                                    )

        if (not email
            or not display_name
            or not password
                or not confirm_password):
            flash("All fields are required!", category="warning")

        elif existing_email:
            flash("Email is already in use.", category="error")

        elif password != confirm_password:
            flash("Passwords don't match!", category="error")

        elif len(display_name) < 3:
            flash("Username is too short.", category="warning")

        elif len(display_name) > 50:
            flash(("Display name is too long. "
                   "Maximum allowed is 50 characters."),
                  category="warning")

        elif len(password) < 6:
            flash("Password is too short.", category="warning")

        elif len(password) > 1024:
            flash("Password is too long. Maximum allowed is 1,024 characters.",
                  category="warning")

        elif validate_email_address(email) == "invalid":
            flash("Invalid email!", category="error")

        else:
            user_id = str(uuid.uuid4())  # Creates a new primary key

            # Creates a random image ID for DiceBear to generate an avatar
            # for the user
            # The reason to not use the user_id,
            #   for this, other users can see
            #   others user_id through their profile image id
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
                       values=(
                           user_id,
                           email,
                           display_name,
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
    """
    Initiate the Google OAuth login flow.

    This route generates a redirect URI and sends the user to Google's
    authorization page for authentication. If an error occurs while
    generating the redirect, it logs the error and returns a 500 response.

    Returns:
        Response: A redirect to Google's OAuth authorization page if
        successful, or a 500 error response if an exception occurs.
    """
    try:
        redirect_uri = url_for("auth.authorize_google", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        current_app.logger.error(f"Error during the logon: {str(e)}")
        return "Error occured during login", 500


@auth_bp.route("/authorize/google")
def authorize_google():
    """
    Handle the Google OAuth callback and log the user into the application.

    This route is called after Google redirects back with an authorization
    code. It exchanges the code for an access token, retrieves user
    information, stores it in the database if the user does not already
    exist, and saves relevant details in the session.

    Returns:
        Response: A redirect to the dashboard after successful login.
    """
    token = google.authorize_access_token()
    session["user"] = token

    user_token = session.get("user")
    user_info = user_token["userinfo"]
    username = user_info["given_name"]
    email = user_info["email"]
    profile_pic = user_info["picture"]
    google_id = user_info["sub"]

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
