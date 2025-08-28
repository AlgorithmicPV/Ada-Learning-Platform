from flask import (Blueprint,
                   render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   jsonify,
                   flash,
                   current_app)
import sqlite3
import uuid
import os
from werkzeug.utils import secure_filename
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from utils import validate_email_address
from PIL import Image
from utils import db_execute, login_required

settings_bp = Blueprint("settings", __name__)

ph = PasswordHasher()

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


# This route shows the setting page
@settings_bp.route("/settings")
@login_required
def settings():
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


# to avoid cyclomatic complexity
# divided into three functions
def update_username(new_username, user_id):
    if new_username.strip() == "":
        return

    if len(new_username) < 2:
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
    # Checks whether user is logged by a gmail account or
    # by a normal account
    # If it is a normal account give access to change the email
    auth_provider = session.get("auth_provider")

    if auth_provider != "manual":
        return

    if new_email.strip() == "":
        flash("Email is already in use.", category="error")
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
        print(email_in_db)
        if email_in_db[0]:
            if email_in_db[0][0] == new_email:
                return

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
        except Exception as e:
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
    new_username = request.form.get("username")
    new_email = request.form.get("email")
    file = request.files.get('image')

    user_id = session.get("user_id")

    update_username(new_username, user_id)
    update_email(new_email, user_id)
    update_profile_image(file, user_id)

    return redirect(url_for("settings.settings"))


def update_password():
    pass


# This route change the Password
@settings_bp.route("/settings/change-password", methods=["POST"])
@login_required
def change_password():
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

            if len(new_password) > 6:
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
            else:
                flash(
                    "Password is too short.", category="error")

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
    user_id = session.get("user_id")

    # Gets the user feedback and star rating
    userfeedback = request.form['comment']
    star = int(request.form['star'])

    # Check whether the user feedback is empty or not
    # This it check the number of stars are in between 0 and 5
    # If all above conditions are satisfied then it will store the
    # feedback in the database
    if not userfeedback == "" and not userfeedback.isspace():
        if star <= 5 and star >= 0:
            id = str(uuid.uuid4())

            insert_query = """
                INSERT INTO User_feedback
                (feedback_id, user_id, feedback, star)
                VALUES (?, ?, ?, ?)
                """

            db_execute(query=insert_query,
                       values=(id, user_id, userfeedback, star))

            return jsonify(
                {'message': (
                 'Thank you for your feedback!'
                 'I really appreciate your time and suggestions.'
                 'It helps me improve and grow.')})
        else:
            return jsonify(
                {'message':
                 'Oops! Ratings can only be between 1 and 5 stars.'})
    else:
        return jsonify(
            {'message': 'Please write some feedback before submitting'})
