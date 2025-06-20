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

# name = "d"
# email = ""

# if not name or not email:
#     print("no name")



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

# from argon2 import PasswordHasher
# from argon2.exceptions import VerifyMismatchError, InvalidHash

# ph = PasswordHasher()

# hash = ph.hash("1234")

# x = input("type the password: ")

# try:
#     if (ph.verify(hash, x)):
#         print("password is correct")
# except VerifyMismatchError:
#     print("Password is not correct")
# except InvalidHash:
#     print("Invalid hash format. The hash may be corrupted")
# # print(x)

import sqlite3

conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()
# email = "vidunithap@gmail.com"
# cursor.execute('SELECT password FROM User WHERE email = ?', (email,))

# stored_has_password = cursor.fetchone()

# print(stored_has_password[0])


cursor.execute("SELECT course_id, course_name, language_image, course_image, language FROM Course")

all_courses_data = cursor.fetchall()

course_data_with_percentage = []

for i in all_courses_data:
    user_id = '5bd134f5-327e-4f3e-8c76-13da3c6f07b5'
    cursor.execute("""SELECT COUNT(lesson_id) FROM user_lesson WHERE user_id  = ? AND lesson_id IN (SELECT lesson_id FROM Lesson WHERE course_id = ?) AND status = 'completed'""", (user_id,i[0],))
    number_of_completed_lessons =  cursor.fetchall()

    number_of_completed_lessons = number_of_completed_lessons[0][0]

    cursor.execute("""SELECT COUNT(*) FROM Lesson WHERE course_id =?""", (i[0],))

    number_of_all_lessons = cursor.fetchall()

    number_of_all_lessons = number_of_all_lessons[0][0]

    if number_of_all_lessons and number_of_completed_lessons:
        percentage_of_the_completion = (number_of_completed_lessons/number_of_all_lessons) * 100
    else:
        percentage_of_the_completion = 0

    for j in range(1 ,5):
        course_data_with_percentage.append(i[j])

    course_data_with_percentage.append(percentage_of_the_completion)


def divide_array_into_chunks(divding_array, chunk_size):
    new_array = []
    for i in range(int((len(divding_array)) / (chunk_size))):
        new_array.append(divding_array[(chunk_size * i): (chunk_size + (chunk_size * i))])
    return new_array

cursor.execute("""SELECT COUNT(*) FROM  Course""")

number_of_courses = cursor.fetchall()[0][0]

divided_array = (divide_array_into_chunks(course_data_with_percentage, number_of_courses ))

for t in divided_array:
    print(t)



#  # cursor.execute(
#         #     """
#         #         SELECT 
#         #           c.course_id,
#         #           c.course_name, 
#         #           c.course_image, 
#         #           c.language, 
#         #           c.language_image,
#         #           ROUND(
#         #             COUNT(ul.lesson_id) * 100.0 / 
#         #             NULLIF((SELECT COUNT(*) FROM Lesson WHERE course_id = c.course_id), 0), 
#         #             0
#         #           ) AS progress_percent
#         #         FROM 
#         #           Course c
#         #         LEFT JOIN 
#         #           Lesson l ON l.course_id = c.course_id
#         #         LEFT JOIN 
#         #           user_lesson ul ON ul.lesson_id = l.lesson_id 
#         #           AND ul.user_id = ?
#         #           AND ul.status = 'completed'
#         #         GROUP BY 
#         #           c.course_id;

#         #     """,
#         #     (session["user_id"],),
#         # )

#         # all_courses_data = cursor.fetchall()

#         cursor.execute()