from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3

my_courses_bp = Blueprint("my_courses", __name__)


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


# This route is used to display all the courses available in the application
@my_courses_bp.route("/my-courses", methods=["GET", "POST"])
def all_courses():
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
                percentage_of_the_completion = round(
                    (number_of_completed_lessons / number_of_all_lessons) * 100
                )  # Calculates the percentage of the completion of the course
            else:
                percentage_of_the_completion = 0

            for j in range(5):  # Appends the course data into a new array
                course_data_with_percentage.append(one_course_set[j])

            course_data_with_percentage.append(
                percentage_of_the_completion
            )  # Appends the percentage of the completion of the course into the new array

        cursor.execute("""SELECT COUNT(*) FROM  Course""")

        number_of_courses = cursor.fetchall()[0][
            0
        ]  # Gets the total number of courses available in the database, and this is used to divide the array into chunks
        divided_array = divide_array_into_chunks(
            course_data_with_percentage,
            int(
                (len(course_data_with_percentage) / number_of_courses)
            ),  # Divdes the length of the course_data_with_percentage by number_of_courses to get the chunk size
        )

        session["all_courses_data"] = divided_array

        if request.method == "POST":
            # remember put an if statement check the validity of the course_id
            course_id = request.form.get("course_id")

            session["course_id"] = course_id

            return redirect(url_for("my_courses.intermediate_route"))
        conn.close()
        return render_template(
            "user/my_courses/all_courses.html", courses_data=divided_array
        )
    else:
        return redirect(url_for("auth.login"))


# This route is used to search for courses based on a keyword entered by the user
@my_courses_bp.route("/my-courses/search", methods=["GET", "POST"])
def search_courses():
    if "user_id" in session:
        all_courses_data = session.get("all_courses_data")
        filtered_courses = (
            []
        )  # This will hold the courses that match the search keyword
        if request.method == "GET":
            keyword = request.args.get(
                "search"
            ).lower()  # Gets the keyword entered by the user and converts it to lowercase for case-insensitive search
            if keyword != " " and keyword != "":
                for course_block in all_courses_data:
                    for word in course_block:
                        word = str(
                            word
                        ).lower()  # Converts each word in the course block to lowercase for case-insensitive search
                        if (
                            keyword in word
                        ):  # Checks if the keyword is present in any word of the course block
                            filtered_courses.append(course_block)
                            break

                return render_template(
                    "user/my_courses/search_result_all_courses.html",
                    courses_data=filtered_courses,
                )  # Uses the same variable name as the original route to reduce the repetition of code in the template
            else:
                return redirect(url_for("my_courses.all_courses"))
    else:
        return redirect(url_for("auth.login"))


@my_courses_bp.route("/my-courses/intermediate", methods=["GET", "POST"])
def intermediate_route():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        course_id = session.get("course_id")
        if request.method == "POST":
            lesson_id = request.form.get("lesson_id")
        else:
            cursor.execute(
                "SELECT lesson_id FROM Lesson WHERE course_id = ?", (course_id,)
            )
            lesson_id = cursor.fetchone()[0]

        cursor.execute("SELECT language FROM Course WHERE  course_id = ?", (course_id,))
        language = cursor.fetchone()[0].lower()
        session['language'] = language
        

        cursor.execute(
            "SELECT lesson_title FROM Lesson WHERE lesson_id=?", (lesson_id,)
        )
        lesson_title = cursor.fetchone()[0]
        session["lesson_title"] = lesson_title

        cursor.execute(
            "SELECT course_name FROM Course WHERE course_id =?", (course_id,)
        )
        course_name = cursor.fetchone()[0]
        session["course_name"] = course_name

        user_id = session.get("user_id")

        cursor.execute(
            "SELECT lesson_id, lesson_title FROM Lesson WHERE course_id = ?",
            (course_id,),
        )
        lessons_data = cursor.fetchall()
        session["lessons_data"] = lessons_data

        cursor.execute(
            """SELECT COUNT(lesson_id) FROM user_lesson WHERE user_id  = ? AND lesson_id IN (SELECT lesson_id FROM Lesson WHERE course_id = ?) AND status = 'completed'""",
            (
                user_id,
                course_id,
            ),
        )
        number_of_completed_lessons = cursor.fetchall()[0][0]
        percentage_of_completion = round(
            (number_of_completed_lessons / len(lessons_data)) * 100
        )
        session["percentage_of_completion"] = percentage_of_completion

        cursor.execute(
            "SELECT content FROM Lesson WHERE lesson_id = ? AND course_id = ?",
            (lesson_id, course_id),
        )
        lesson_content = cursor.fetchall()
        session["lesson_content"] = lesson_content[0][0]

        formated_course_name = "-".join(
                course_name.split(" ")
            ) 
        
        formated_lesson_name = "-".join(
                lesson_title.split(" ")
            ) 

        return redirect(
            url_for(
                "my_courses.lesson", course_name=formated_course_name, lesson_name=formated_lesson_name
            )
        )


@my_courses_bp.route("/my-courses/<course_name>/<lesson_name>", methods=["GET", "POST"])
def lesson(course_name, lesson_name):
    if "user_id" in session:
        return render_template(
            "user/my_courses/lesson.html",
            course_name=session.get("course_name"),
            lesson_title=session.get("lesson_title"),
            lessons_data=session.get("lessons_data"),
            percentage_of_completion=session.get("percentage_of_completion"),
            lesson_content=session.get("lesson_content"),
            language = session.get("language")
        )
    else:
        return redirect(url_for("auth.login"))


# This route is used to display the AI-generated courses
@my_courses_bp.route("/my-courses/ai_generated", methods=["GET", "POST"])
def ai_courses():
    if "user_id" in session:
        return render_template("user/my_courses/ai_generated_courses.html")
    else:
        return redirect(url_for("auth.login"))


# This route is used to display the courses that the user has completed
@my_courses_bp.route("/my-courses/completed-courses", methods=["GET", "POST"])
def completed_courses():
    if "user_id" in session:
        return render_template("user/my_courses/completed_courses.html")
    else:
        return redirect(url_for("auth.login"))
