from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash, current_app
import sqlite3
import uuid
from datetime import datetime, date
import string
import os
from werkzeug.utils import secure_filename
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from utils import validate_email_address


settings_bp = Blueprint("settings", __name__)

ph = PasswordHasher()

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS

# This route shows the setting page


@settings_bp.route("/settings")
def settings():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        auth_provider = session.get("auth_provider")

        user_id = session.get("user_id")

        cursor.execute(
            "SELECT full_name, email, profile_image FROM User WHERE user_id=?", (user_id,))

        user_data = cursor.fetchall()
        if user_data:
            user_data = user_data[0]

        return render_template(
            "user/settings.html",
            user_data=user_data,
            auth_provider=auth_provider)
    else:
        return redirect(url_for("auth.login"))

# This route updates the username, the email and the profile image of the user


@settings_bp.route("/settings/profile-update", methods=["POST"])
def profile_update():
    if "user_id" in session:
        if request.method == "POST":
            new_username = request.form.get("username")
            new_email = request.form.get("email")

            user_id = session.get("user_id")

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Gets the current email of the user from the database
            cursor.execute("""
                    SELECT email FROM User
                    WHERE user_id=?
                    """, (user_id,))

            current_email = cursor.fetchone()[0]

            # Checks if the username and email are not empty
            if not new_username == "" and not new_username.isspace():
                # If the new username has more than two characters
                # Before updating the database
                # If not, sends a flash message to the frontend saying Username
                # is too short
                if len(new_username) > 2:
                    cursor.execute("""
                                UPDATE User
                                SET full_name = ?
                                WHERE user_id=?  AND full_name != ?
                                    """, (new_username, user_id, new_username))
                    if cursor.rowcount != 0:
                        flash(
                            "Username updated successfully!",
                            category="success")
                    conn.commit()
                else:
                    flash("Username is too short.", category="error")

            # Checks whether user is logged by a gmail account or
            # by a normal account
            # If it is a normal account give access to change the email
            auth_provider = session.get("auth_provider")
            if auth_provider == "manual":
                if not new_email == "" and not new_email.isspace():
                    # Checks the new email is in the database
                    cursor.execute("""SELECT email
                                    FROM User
                                    WHERE email=?""", (new_email,))
                    email_from_db = cursor.fetchone()
                    # if the database output is None,
                    # It will check does new email have @ mark
                    # If the email doesn't have @ mark, it will send a flash
                    # message to the frontend saying Invalid email
                    if email_from_db is None:
                        validate_email = validate_email_address(new_email)
                        if validate_email == "invalid":
                            flash("Invalid email!", category="error")
                        else:
                            cursor.execute("""
                                        UPDATE User
                                        SET email = ?
                                        WHERE user_id=? AND email != ?
                                            """, (new_email, user_id, new_email))

                            flash(
                                "Your email address has been updated",
                                category="success")

                            conn.commit()
                    # IF the new email is same as the current email, it will
                    # pass
                    elif email_from_db[0] == current_email:
                        pass
                    else:
                        flash("Email is already in use.", category="error")

            # Gets the users' new profile image to update
            file = request.files.get('image')

            # Validates the file
            if file and file.filename != '':

                # validates the file type is an image
                ext = os.path.splitext(file.filename)[1].lower()

                if ext in ALLOWED_EXTENSIONS:
                    # Doesn't use the file name of the uploaded image
                    # because it will cause overwritting another file with the same file name
                    # Therefore uses uuid4 generated code for the filename
                    filename = secure_filename(str(uuid.uuid4())) + ext

                    # Saves the image to the static folder
                    upload_folder = os.path.join(
                        current_app.root_path, 'static', 'images', 'profile_pics')
                    os.makedirs(upload_folder, exist_ok=True)

                    save_path = os.path.join(upload_folder, filename)
                    file.save(save_path)

                    # Updates the database with the new profile image location
                    profile_image = f"images/profile_pics/{filename}"

                    cursor.execute("""
                            UPDATE USER
                            SET profile_image=?
                            WHERE user_id=?
                                """, (profile_image, user_id,))
                    flash(
                        "Looking good! Your profile picture has been updated.",
                        category="success")
                    conn.commit()
                else:
                    flash("Invalid image format.", category="error")

                conn.close()

            return redirect(url_for("settings.settings"))

    else:
        return redirect(url_for("auth.login"))


# This route change the Password
@settings_bp.route("/settings/change-password", methods=["POST"])
def change_password():
    if "user_id" in session:
        if request.method == "POST":
            user_id = session.get("user_id")

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Gets the data from the clienst side and
            # Saves it to below three varaibles
            current_password = request.form.get("currentPassword")
            new_password = request.form.get("new-password")
            new_confirm_password = request.form.get("confirm-new-password")

            # Gets the actual hashed password that related to the logged in
            # user
            cursor.execute("""
                        SELECT password
                        FROM User
                        WHERE user_id=?
                        """, (user_id,))
            stored_hash_password = cursor.fetchone()

            # Checks whether user is logged by a gmail account or
            # by a normal account
            # If it is a gmail account send a flash messeage saying
            # "Users signed in via Google cannot update their password here"
            auth_provider = session.get("auth_provider")
            if auth_provider == "manual":

                # Verify the current_password with the stored hashed password
                # If it is true then it will update the password
                if stored_hash_password:
                    try:
                        if ph.verify(
                                stored_hash_password[0],
                                current_password):
                            # Check the typed New Password and the confirm Password is equal or not
                            # IF it is equal then it will count the characters in the new password
                            # If it is greater than 6 then it will update the password
                            # Otherise It will send a flash message to the
                            # frontend saying "Password is too short"
                            if new_password == new_confirm_password:
                                if len(new_password) > 6:
                                    cursor.execute("""
                                                UPDATE User
                                                SET password =?
                                                WHERE user_id=?
                                                    """, (ph.hash(new_password), user_id))
                                    conn.commit()
                                    flash(
                                        "Password changed successfully. You are all set!",
                                        category="success")
                                else:
                                    flash(
                                        "Password is too short.", category="error")
                            # IF passwords are not equal then it will send a
                            # flash message to the frontend saying "Password
                            # are not matched"
                            else:
                                flash(
                                    "Password are not matched", category="error")
                    except (VerifyMismatchError):  # If the password does not match the stored hash
                        flash("Password is not correct", category="error")

                    except InvalidHash:  # If the password hash is invalid
                        flash(
                            "Invalid hash format. The hash may be corrupted",
                            category="error")

                    except Exception as e:  # Catch any other exceptions
                        flash(f"An error occured: {e}", category="error")
                else:
                    flash("Password is not correct", category="error")
            else:
                flash(
                    "Users signed in via Google cannot update their password here",
                    category="error")
        conn.close()
        return redirect(url_for("settings.settings"))
    else:
        return redirect(url_for("auth.login"))

# This route is used to delete the user account permenantly from all the tables


@settings_bp.route("/settings/delete-account", methods=["POST"])
def delete_account():
    if "user_id" in session:
        if request.method == "POST":
            user_id = session.get("user_id")

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            delete = request.form.get("delete")

            if delete == "delete":
                cursor.execute(
                    "DELETE FROM AI_resource WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM Answer WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM Challenge_attempt WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM User_feedback WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM Question WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM Saved_question WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM Enrollment WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM User_lesson WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM AnswerLike WHERE user_id = ?", (user_id,))
                cursor.execute(
                    "DELETE FROM User WHERE user_id = ?", (user_id,))
                session.clear()
                conn.commit()
                conn.close()
        return redirect(url_for("settings.settings"))
    else:
        return redirect(url_for("auth.login"))

# THis route is used to get feedback from the user


@settings_bp.route("/settings/get-feedback", methods=["POST"])
def feedback():
    if "user_id" in session:
        if request.method == "POST":
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

                    conn = sqlite3.connect("database/app.db")
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO User_feedback
                        (feedback_id, user_id, feedback, star)
                        VALUES (?, ?, ?, ?)
                        """, (id, user_id, userfeedback, star))

                    conn.commit()
                    conn.close()

                    return jsonify(
                        {'message': 'Thank you for your feedback! I really appreciate your time and suggestions. It helps me improve and grow.'})
                else:
                    return jsonify(
                        {'message': 'Oops! Ratings can only be between 1 and 5 stars.'})

            else:
                return jsonify(
                    {'message': 'Please write some feedback before submitting'})

    else:
        return redirect(url_for("auth.login"))
