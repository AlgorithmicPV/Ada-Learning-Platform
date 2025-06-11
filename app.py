from flask import Flask, render_template, redirect, request, url_for, flash, session
import sqlite3
from datetime import datetime
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash


app = Flask(__name__)

app.secret_key = "test123"

ph = PasswordHasher()


# Landing Page
@app.route("/")
def landing():
    return render_template("landing_page.html")


# login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM User WHERE email = ?", (email,))
        stored_hash_password = cursor.fetchone()

        cursor.close()

        if stored_hash_password:
            try:
                if ph.verify(stored_hash_password[0], password):
                    return redirect(url_for("dashboard"))
            except VerifyMismatchError:
                flash("Password is not correct", category="error")
                return redirect(url_for("login"))
            except InvalidHash:
                flash(
                    "Invalid hash format. The hash may be corrupted", category="error"
                )
                return redirect(url_for("login"))
        else:
            flash("Username doesn't exist", category="error")
            return redirect(url_for("login"))

    return render_template("login.html")


# Create an account page
@app.route("/signup", methods=["GET", "POST"])
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
                (user_id, email, name, ph.hash(password), "manual", "dark", timestamp),
            )

            conn.commit()
            cursor.close()

            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
