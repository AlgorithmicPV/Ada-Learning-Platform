# import uuid
# import sqlite3
# from datetime import datetime

# conn = sqlite3.connect("database/app.db")
# cursor = conn.cursor()

# cursor.execute("""SELECT email FROM User""")

# email_list = cursor.fetchall()

# saved_emails = []


# for email_tuple in email_list:
#     for email in email_tuple:
#         saved_emails.append(email)

# print(saved_emails)

# if "vidunithap@gmail.com" in saved_emails:
#     print("it is there")

# # cursor.execute("""SELECT full_name FROM User""")

# # name_rows = cursor.fetchall()

# # print(name_rows)

# conn.close()

# text = "test@gmail.com"

# text_t = "testgmail.com"

# if "@" in text_t:
#     print("valid email")
# else:
#     print("not valid")

name = "d"
email = ""

if not name or not email:
    print("no name")



# # Create an account page
# @app.route("/signup", methods=["GET", "POST"])
# def signup():

#     if request.method == "POST":
#         email = request.form.get("email")
#         name = request.form.get("name")
#         password = request.form.get("password")
#         confirm_password = request.form.get("confirm-password")

#         session["email"] = email
#         session["name"] = name

#         if password != confirm_password:
#             flash("Passwords do not match", "error")
#             error_status = "error"
#             return redirect(
#                 url_for("signup")
#             )  # Used redirect after POST to follow the Post-Redirect-Get (PRG) pattern and prevent form resubmission warning on page reload
#         else:
#             pass

#         if not name or not email or not password or not confirm_password:

#             return redirect(
#                 url_for("signup", error_with_fields="All fields are required!")
#             )  # Used redirect after POST to follow the Post-Redirect-Get (PRG) pattern and prevent form resubmission warning on page reload
#         else:
#             pass

#         return redirect(url_for("signup"))


#     saved_name = session.pop("name", default=None)
#     saved_email = session.pop("email", default=None)
#     # print(error_status)

#     return render_template("signup.html")

# ##signup
# @app.route("/test", methods = ["GET", "POST"])
# def test():
#     if request.method == "POST":
#         email = request.form.get("email")
#         name = request.form.get("name")
#         password = request.form.get("password")
#         c_password = request.form.get("confirm-password")

#         print(email, name, password, c_password)

#         if password != c_password:
#             print("passwords are not the same")
#             return render_template("test.html", email = email,name = name )

#         return redirect(url_for("test"))

#     return render_template("test.html")