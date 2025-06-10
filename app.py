from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import uuid


app = Flask(__name__)

app.secret_key = "test123"


# Landing Page
@app.route("/")
def landing():
    return render_template("landing_page.html")


# login page
@app.route("/login", methods=["GET", "POST"])
def login():
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

        saved_names = [] # An array to collect all the names from the database

        # Converts the full_name_list into a flat array to easily check if the entered name is valid or not. full_name_list is a list of 1-element tuples
        for name_tuple in full_name_list:
            for name_from_db in name_tuple:
                saved_names.append(name_from_db)

        conn.close()

        if not email or not name or not password or not confirm_password:
            print("All fields are required!")
            flash("All fields are required!", category="error")

        elif email in saved_emails:
            print("Email is already in use.")
            flash("Email is already in use.", category="error")

        elif name in saved_names:
            print("Username is already in use.")
            flash("Username is already in use.", category="error")

        elif password != confirm_password:
            print("Passwords don't match!")
            flash("Passwords don't match!", category="error")

        elif len(name) < 2:
            print("Username is too short.")
            flash("Username is too short.", category="error")

        elif len(password) < 6:
            print("Password is too short.")
            flash("Password is too short.", category="error")

        elif "@" not in email:
            print("Invalid email!")
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
                (user_id, email, name, password, "manual", "dark", timestamp),
            )

            conn.commit()

            cursor.close()

            return redirect(url_for("login"))

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
