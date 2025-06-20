from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3

my_courses_bp = Blueprint("my_courses", __name__)


@my_courses_bp.route("/my-courses", methods=["GET", "POST"])
def all_course():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        user_id = session["user_id"]

        cursor.execute(
            "SELECT course_id, course_name, language_image, course_image, language FROM Course"
        )

        all_courses_data = cursor.fetchall()

        course_data_with_percentage = []

        for (
            one_course_set
        ) in all_courses_data:  # Fetches all the courses data from the database
            cursor.execute(
                """SELECT COUNT(lesson_id) FROM user_lesson WHERE user_id  = ? AND lesson_id IN (SELECT lesson_id FROM Lesson WHERE course_id = ?) AND status = 'completed'""",
                (
                    user_id,
                    one_course_set[0],
                ),
            )  # Selects all the completed lessons (number)

            number_of_completed_lessons = cursor.fetchall()

            number_of_completed_lessons = number_of_completed_lessons[0][
                0
            ]  #  Converts into a flat variable as the previous variable "number_of_completed_lessons" is a list of one element

            cursor.execute(
                """SELECT COUNT(*) FROM Lesson WHERE course_id =?""",
                (one_course_set[0],),
            )  # Gets the total number of lessons available in  a course the database

            number_of_all_lessons = (
                cursor.fetchall()
            )  # Gets the total number of lessons available in a course the database

            number_of_all_lessons = number_of_all_lessons[0][0]

            if number_of_all_lessons and number_of_completed_lessons:
                percentage_of_the_completion = round((
                    number_of_completed_lessons / number_of_all_lessons
                ) * 100) # Calculates the percentage of the completion of the course
            else:
                percentage_of_the_completion = 0

            for j in range(5):  # Appends the course data into a new array
                course_data_with_percentage.append(one_course_set[j])
                # print(one_course_set[5])

            course_data_with_percentage.append(
                percentage_of_the_completion
            )  # Appends the percentage of the completion of the course into the new array

        # Function to divide an array into chunks of a specified size
        # This is used to display the courses in a grid format on the frontend
        def divide_array_into_chunks(
            dividing_array, chunk_size
        ):  # Divides an array into chunks of a specified size
            new_array = []
            for i in range(
                int(
                    (len(dividing_array)) / (chunk_size)
                )  # Calculates the number of chunks needed by dividing the length of the array by the chunk size and converting it to an integer as it is a float value
            ):  # Iterates over the array in chunks
                new_array.append(
                    dividing_array[
                        (chunk_size * i) : (chunk_size + (chunk_size * i))
                    ]  # {chunk_size * i} is the starting index of the chunk, and {chunk_size + (chunk_size * i)} is the ending index of the chunk
                )  # Appends the chunk to the new array,
            return new_array

        cursor.execute("""SELECT COUNT(*) FROM  Course""")

        number_of_courses = cursor.fetchall()[0][0]  # Gets the total number of courses available in the database, and this is used to divide the array into chunks
        divided_array = divide_array_into_chunks(
            course_data_with_percentage, int((len(course_data_with_percentage) / number_of_courses)) # Divdes the length of the course_data_with_percentage by number_of_courses to get the chunk size
        )

        return render_template("user/my_courses/all_courses.html", all_courses_data=divided_array)
    else:
        return redirect(url_for("auth.login"))


@my_courses_bp.route("/my-courses/completed", methods=["GET", "POST"])
def completed_courses():
    return render_template("user/my_courses/completed_courses.html")

@my_courses_bp.route("/my-courses/ai_generated", methods=["GET", "POST"])
def ai_courses():
    return render_template("user/my_courses/ai_generated_courses.html")
