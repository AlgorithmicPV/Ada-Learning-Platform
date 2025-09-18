"""
Handles all the user setting page
"""

import os
import uuid
from flask import (Blueprint,
                   render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   jsonify,
                   flash,
                   current_app)
from werkzeug.utils import secure_filename
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from PIL import Image
from utils import (db_execute,
                   login_required,
                   validate_email_address,
                   check_characters_limit)

settings_bp = Blueprint("settings", __name__)

ph = PasswordHasher()

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg'}


def allowed_file(filename):
    """
    This function checks whether a given filename has an allowed extension.

    Process:
        - Verifies the presence of a "." in the filename.
        - Splits the filename at the last "." to extract the extension.
        - Compares the extracted extension (in lowercase) against the set
          of ALLOWED_EXTENSIONS.

    Args:
        filename (str): The name of the file to validate.

    Returns:
        - bool: True if the file extension is in ALLOWED_EXTENSIONS,
        otherwise False.
    """
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# This route shows the setting page
@settings_bp.route("/settings")
@login_required
def settings():
    """
    This route displays the settings page for the logged-in user.

    The function gets the authentication provider and user_id
    from the session, executes a SQL query to fetch the
    user's full name, email, and profile image, and prepares the data
    if available. It then renders the "user/settings.html"
    template, passing both the user data
    and the authentication provider for display.


    Returns:
         - Rendered HTML template "user/settings.html"
         containing user settings data.
    """
    auth_provider = session.get("auth_provider")

    user_id = session.get("user_id")

    query = """
            SELECT
                full_name,
                email,
                profile_image
            FROM User
            WHERE user_id=?"""

    user_data = db_execute(query=query,
                           fetch=True,
                           values=(user_id,))
    if user_data:
        user_data = user_data[0]

    return render_template(
        "user/settings.html",
        user_data=user_data,
        auth_provider=auth_provider)


# To avoid cyclomatic complexity
# created update_username(), update_email(),
#   update_profile_image()
# divided into three functions
def update_username(new_username, user_id):
    """
    This function updates the username of a user in the database.

    It first checks that the new username is not empty and has a valid length.
    The function then queries the database to confirm whether the
    existing username is different from the provided one.
    If the username is unchanged, the update is skipped.
    Otherwise, it executes an update query to modify the user's full name
    and flashes a success message to indicate the update was completed.

    Args:
        new_username (str): The new username provided by the user.
        user_id (int): The unique identifier of the user whose username
                       is being updated.

    Returns:
        - flashes messages to indicate the result.
    """
    if new_username.strip() == "":
        flash("Username is empty", category="warning")
        return

    # validates the number of characters
    character_limit_result = check_characters_limit(new_username,
                                                    max_length=50,
                                                    min_length=3)
    if character_limit_result == "max_result":
        flash(("Display name is too long. "
               "Maximum allowed is 50 characters."),
              category="warning")
        return

    elif character_limit_result == "min_result":
        flash("Username is too short.", category="error")
        return

    username_query = """
                    SELECT
                        full_name
                    FROM
                        User
                    WHERE user_id = ?
                    """
    username = db_execute(query=username_query,
                          fetch=True,
                          fetchone=True,
                          values=(user_id, ))

    # if the prev username is equal to types username,
    # nothing happens
    # otheriwse, user gets a message that username was updated
    # which can cause confusion for users
    if username:
        if username[0] == new_username:
            return

    update_query = """
                    UPDATE User
                    SET full_name = :new_name
                    WHERE user_id= :uid  AND full_name != :new_name
                """

    db_execute(query=update_query,
               values={"new_name": new_username,
                       "uid": user_id})
    flash(
        "Username updated successfully!",
        category="success")


def update_email(new_email, user_id):
    """
    This function updates the email address of a user in the database.

    It first checks the authentication provider from the session to ensure
    the user is logged in with a manual account before allowing changes.
    The function then validates the new email, checking that it is not empty
    and has a valid format. It queries the database to confirm that the new
    email is not the same as the current one and is not already used
    by another user.If these checks pass, the user's email is updated
    in the database, and a success message is flashed. Otherwise,
    appropriate error messages are shown.

    Args:
        new_email (str): The new email address provided by the user.
        user_id (int): The unique identifier of the user whose email
                       is being updated.

    Returns:
        - flashes messages to indicate the result.
    """
    # Checks whether user is logged by a gmail account or
    # by a normal account
    # If it is a normal account give access to change the email
    auth_provider = session.get("auth_provider")

    if auth_provider != "manual":
        return

    if new_email.strip() == "":
        flash("Email cannot be empty", category="warning")
        return

    if validate_email_address(new_email) == "invalid":
        flash("Invalid email!", category="error")
        return

    email_in_db_query = """
                        SELECT
                            (SELECT email
                            FROM User
                            WHERE user_id = :uid)
                            AS current_email,
                            (SELECT 1 FROM
                            User WHERE email = :email
                            AND user_id != :uid)
                            AS email_exists;
                        """

    email_in_db = db_execute(query=email_in_db_query,
                             fetch=True,
                             values={"uid": user_id,
                                     "email": new_email})

    if email_in_db:
        # if the typed email == new email,
        # returning from the route
        # otherwise, user is getting a message
        # that email is updated
        # which can cause confusion for users
        # email_in_db[0][0] mean user's prev email
        if email_in_db[0]:
            if email_in_db[0][0] == new_email:
                return
            # email_in_db[0][1] means other emails that equals
            # to the typed email
            if email_in_db[0][1]:
                flash("Email is already in use.", category="error")
                return

    update_email_query = """
                        UPDATE User
                        SET email = :email
                        WHERE user_id = :uid
                        AND email != :email
                        AND NOT EXISTS (
                            SELECT 1
                            FROM User
                            WHERE email = :email
                            AND user_id != :uid
                        );
                        """

    db_execute(query=update_email_query,
               values={"email": new_email,
                       "uid": user_id})

    flash(
        "Your email address has been updated",
        category="success")


def update_profile_image(file, user_id):
    """
    This function updates the profile image of a user in the database.

    It first checks that a file has been uploaded and validates that
    the file type is a supported image format. A secure,
    unique filename is generated, and the image is saved into the
    designated profile pictures folder. If the user already has a
    locally stored profile image, the previous file is deleted to keep the
    project clean. The new image is then converted and stored in
    WebP format for optimization, and the relative image path is updated
    in the database. Finally, a success message is flashed,
    or an error message is shown if the upload fails.

    Args:
        file (FileStorage): The uploaded image file provided by the user.
        user_id (int): The unique identifier of the user whose profile
                       image is being updated.

    Returns:
        - flashes messages to indicate the result.
    """
    if not file:
        return

    ext = os.path.splitext(file.filename)[1].lower()

    # validates the file type is an image
    if ext not in ALLOWED_EXTENSIONS:
        flash("Invalid image format.", category="error")
        return

    base_filename = secure_filename(str(uuid.uuid4()))

    # Define upload/output folder
    upload_folder = os.path.join(
        current_app.root_path, 'static', 'images', 'profile_pics')
    os.makedirs(upload_folder, exist_ok=True)

    image_source = session.get("image_source")

    if image_source == "local":

        profile_img_query = """
                            SELECT profile_image
                            FROM USER
                            WHERE user_id = ?
                            """

        prev_iamge_tuple = db_execute(query=profile_img_query,
                                      fetch=True,
                                      fetchone=False,
                                      values=(user_id, ))

        # Delete the previous image
        # to keep the project clean
        if prev_iamge_tuple:
            os.remove(f'static/{prev_iamge_tuple[0]}')

    if ext == '.webp':
        webp_filename = base_filename + ".webp"
        webp_path = os.path.join(upload_folder, webp_filename)
        profile_image = f"images/profile_pics/{webp_filename}"
        file.save(webp_path, quality=90, optimize=True)
    else:
        # Generate unique filename
        original_filename = base_filename + ext
        webp_filename = base_filename + ".webp"

        # Paths
        original_path = os.path.join(
            upload_folder, original_filename)
        webp_path = os.path.join(upload_folder, webp_filename)

        # Save original temporarily
        file.save(original_path)

        try:
            # Open and convert
            image = Image.open(original_path)
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            image.save(
                webp_path, "WEBP", quality=90, optimize=True)

            # Optional: delete original image
            os.remove(original_path)
        except Exception:
            flash(
                "Image upload failed. Try again with a different file.",
                category="error")
            return

        # Save relative webp path to DB
        profile_image = f"images/profile_pics/{webp_filename}"

    update_query = """
                UPDATE USER
                SET profile_image = ?
                WHERE user_id = ?
                """

    db_execute(query=update_query,
               values=(profile_image,
                       user_id))

    flash(
        "Looking good! Your profile picture has been updated.",
        category="success")


# This route updates the username, the email and the profile image of the user
@settings_bp.route("/settings/profile-update", methods=["POST"])
@login_required
def profile_update():
    """
    This route updates the username, email, and profile image
    of the logged-in user.

    It calls above functions

    Returns:
        Response: A redirect response to the settings page.
    """
    new_username = request.form.get("username")
    new_email = request.form.get("email")
    file = request.files.get('image')

    user_id = session.get("user_id")

    update_username(new_username, user_id)
    update_email(new_email, user_id)
    update_profile_image(file, user_id)

    return redirect(url_for("settings.settings"))


# This route change the Password
@settings_bp.route("/settings/change-password", methods=["POST"])
@login_required
def change_password():
    """
    This route lets a logged-in user change their account password.

    The function reads the current password, new password,
    and confirm password from the form, and gets the user_id
    and auth provider from the session. If the user signed in with Google,
    it stops and shows an error because Google users cannot
    change passwords here. It then loads the stored password hash
    from the database and verifies it against the current password.
    If the current password is correct, it checks that the
    new password matches the confirm field and is longer than 6 characters.
    When all checks pass, it updates the password in the database
    and shows a success message. Any failed check shows a clear error message.
    In all cases, the user is redirected back to the settings page.
    Passwords should be in limits


    Returns:
        - A redirect back to the settings page,
          with flashed messages indicating the result.
    """
    user_id = session.get("user_id")

    # Gets the data from the clienst side and
    # Saves it to below three varaibles
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("new-password")
    new_confirm_password = request.form.get("confirm-new-password")

    # Gets the actual hashed password that related to the logged in
    # user
    password_query = """
                SELECT password
                FROM User
                WHERE user_id=?
                """
    stored_hash_password = db_execute(query=password_query,
                                      fetch=True,
                                      fetchone=True,
                                      values=(user_id,))

    # Checks whether user is logged by a gmail account or
    # by a normal account
    # If it is a gmail account send a flash messeage saying
    # "Users signed in via Google cannot update their password here"
    auth_provider = session.get("auth_provider")
    if auth_provider != "manual":
        flash(
            "Users signed in via Google cannot update their password here",
            category="error")
        return redirect(url_for("settings.settings"))

    # Verify the current_password with the stored hashed password
    # If it is true then it will update the password
    if not stored_hash_password:
        flash("Password is not correct", category="error")
        return redirect(url_for("settings.settings"))

    try:
        if ph.verify(
                stored_hash_password[0],
                current_password):
            # Check the typed New Password and
            # the confirm Password is equal or not
            # IF it is equal then
            # it will count the characters in the new password
            # IF passwords are not equal then it will send a
            # flash message to the frontend saying "Password
            # are not matched"
            # If it is greater than 6 then it will update the password
            # Otherise It will send a flash message to the
            # frontend saying "Password is too short"
            if new_password != new_confirm_password:
                flash("Password are not matched",
                      category="error")
                return redirect(url_for("settings.settings"))

            check_characters_result = check_characters_limit(new_password,
                                                             max_length=1024,
                                                             min_length=6)

            if check_characters_result == "max_reject":
                flash("Password is too small", category="warning")
                return

            elif check_characters_result == "min_reject":
                flash(("Password is too long. "
                       "Maximum allowed is 1,024 characters."),
                      category="warning")
                return

            update_query = """
                        UPDATE User
                        SET password =?
                        WHERE user_id=?
                            """

            db_execute(query=update_query,
                       values=(ph.hash(new_password), user_id))
            flash(
                "Password changed successfully. You are all set!",
                category="success")

    # If the password does not match the stored hash
    except (VerifyMismatchError):
        flash("Password is not correct", category="error")

    except InvalidHash:  # If the password hash is invalid
        flash(
            "Invalid hash format. The hash may be corrupted",
            category="error")

    except Exception as e:  # Catch any other exceptions
        flash(f"An error occured: {e}", category="error")

    return redirect(url_for("settings.settings"))


# This route is used to delete the user account permenantly from all the tables
@settings_bp.route("/settings/delete-account", methods=["POST"])
@login_required
def delete_account():
    """
    This route deletes the user account permanently from all related tables.

    The function gets the user_id from the session and checks the form
    input to confirm the delete action. If the confirmation is correct,
    it loops through all tables linked to the user and removes every record
    that matches the user_id. After deleting the data, the session is cleared
    to log the user out, and the function redirects back to the
    settings page, As there is no user_id in the session,
    it automatically redirects again to the login page


    Returns:
        - A redirect back to the settings page
          after the account is deleted.
    """
    user_id = session.get("user_id")

    delete = request.form.get("delete")

    if delete == "delete":
        tables = ['AI_resource',
                  'Answer',
                  'Challenge_attempt',
                  'User_feedback',
                  'Question',
                  'Saved_question',
                  'Enrollment',
                  'User_lesson',
                  'AnswerLike',
                  'User']

        for table in tables:
            delete_query = f"""
            DELETE FROM {table} WHERE user_id = ?
            """
            db_execute(query=delete_query,
                       values=(user_id, ))

        session.clear()
        return redirect(url_for("settings.settings"))


# THis route is used to get feedback from the user
@settings_bp.route("/settings/get-feedback", methods=["POST"])
@login_required
def feedback():
    """
    This route saves user feedback and a star rating.

    The function reads the comment and star value from the form,
    gets the user_id from the session, and ignores empty or
    whitespace-only comments. It then validates the comment length
    (10-300 chars) using check_characters_limit and shows a warning if it
    is too short or too long. If the star rating is within the allowed range,
    it creates a new feedback record with a UUID and stores
    it in the User_feedback table. On success, it returns a
    JSON thank-you message; otherwise
    it returns a JSON message explaining the issue.


    Returns:
        - Response: JSON message indicating success or the validation error.
    """
    user_id = session.get("user_id")

    # Gets the user feedback and star rating
    user_feedback = request.form['comment']
    star = int(request.form['star'])

    # Check whether the user feedback is empty or not
    # This it check the number of stars are in between 0 and 5
    # If all above conditions are satisfied then it will store the
    # feedback in the database
    if not user_feedback == "" and not user_feedback.isspace():

        # validates the limmits
        characters_limit_result = check_characters_limit(user_feedback,
                                                         max_length=300,
                                                         min_length=10)

        if characters_limit_result == "min_reject":
            flash(("Feedback is too short. "
                   "Please provide at least 10 characters."),
                  category="warning")
            return

        elif characters_limit_result == "max_reject":
            flash(("Feedback is too long. "
                   "Please keep it under 300 characters."),
                  category="warning")
            return

        if star <= 5 and star >= 0:
            feedback_id = str(uuid.uuid4())

            insert_query = """
                INSERT INTO User_feedback
                (feedback_id, user_id, feedback, star)
                VALUES (?, ?, ?, ?)
                """

            db_execute(query=insert_query,
                       values=(feedback_id, user_id, user_feedback, star))

            return jsonify(
                {'message': (
                 'Thank you for your feedback!'
                 'I really appreciate your time and suggestions.'
                 'It helps me improve and grow.')})
        else:
            return jsonify(
                {'message':
                 'Oops! Ratings can only be between 0 and 5 stars.'})
    else:
        return jsonify(
            {'message': 'Please write some feedback before submitting'})
