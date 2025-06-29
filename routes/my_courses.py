from flask import Blueprint, render_template, session, redirect, url_for, request, abort
import sqlite3
from datetime import datetime
import uuid


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
                    one_course_set[0], #Course ID
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

            cursor.execute("SELECT course_id FROM Course")

            course_id_tuple = cursor.fetchall()

            course_ids = []

            for element in course_id_tuple:
                for course_id in element:
                    course_ids.append(course_id)

            course_id = request.form.get("course_id")

            if course_id not in course_ids:
                abort(404)

            session["course_id"] = course_id

            session["lesson_order"] = 1

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


# This route is to process all the lesson data and works as an intermediate route between the all_courses route and the lesson route.
# It fetches the lesson data from the database and stores it in the session for later use
@my_courses_bp.route("/my-courses/intermediate", methods=["GET", "POST"])
def intermediate_route():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        course_id = session.get("course_id")
        if (
            request.method == "POST"
        ):  # If the request method is POST, it means the user has selected a lesson
            lesson_id = request.form.get("lesson_id")
        else:  # else, it means the user has not selected a lesson yet

            lesson_order_number = session.get(
                "lesson_order"
            )  # Gets the lesson order number from the session, which is set to 1 by default but can be changed by the user

            cursor.execute(
                "SELECT lesson_id FROM Lesson WHERE course_id = ? AND lesson_order = ?",
                (
                    course_id,
                    lesson_order_number,
                ),
            )
            lesson_id = cursor.fetchone()[0]

        session["lesson_id"] = lesson_id

        cursor.execute("SELECT language FROM Course WHERE  course_id = ?", (course_id,))
        language = cursor.fetchone()[0]
        session["language"] = language

        cursor.execute(
            "SELECT lesson_title FROM Lesson WHERE lesson_id=?", (lesson_id,)
        )
        lesson_titles = cursor.fetchone()

        if not lesson_titles:
            abort(404)

        lesson_title = lesson_titles[0]

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
        )  # Formats the course name by replacing spaces with hyphens for URL compatibility

        formated_lesson_name = "-".join(
            lesson_title.split(" ")
        )  # Formats the lesson name by replacing spaces with hyphens for URL compatibility

        cursor.execute(
            "SELECT COUNT(lesson_order) FROM Lesson WHERE course_id =?",
            (course_id,),
        )

        number_of_lessons = cursor.fetchone()[0]

        cursor.execute(
            "SELECT lesson_order FROM Lesson WHERE lesson_id = ? AND course_id =?",
            (lesson_id, course_id),
        )

        # Find the next and previous lesson IDs based on the current lesson order number
        # This is used to navigate between lessons in the course , which is useful for the user to navigate through the lessons easily
        current_lesson_order_number = cursor.fetchone()[0]

        next_lesson_order_number = current_lesson_order_number + 1

        prev_lesson_order_number = current_lesson_order_number - 1

        # If the next lesson order number is less than or equal to the total number of lessons, fetch the next lesson ID otherwise set it to the current lesson ID
        if next_lesson_order_number <= number_of_lessons:
            cursor.execute(
                "SELECT lesson_id FROM Lesson WHERE lesson_order = ? AND course_id =?",
                (next_lesson_order_number, course_id),
            )
            next_lesson_id = cursor.fetchone()[0]
            session["next_lesson_id"] = next_lesson_id
        else:
            session["next_lesson_id"] = lesson_id

        # If the previous lesson order number is greater than 0, fetch the previous lesson ID otherwise set it to the current lesson ID
        # This is to ensure that the user can navigate back to the previous lesson if they are not on the first lesson
        if prev_lesson_order_number != 0:
            cursor.execute(
                "SELECT lesson_id FROM Lesson WHERE lesson_order = ? AND course_id =?",
                (prev_lesson_order_number, course_id),
            )
            prev_lesson_id = cursor.fetchone()[0]
            session["prev_lesson_id"] = prev_lesson_id
        else:
            session["prev_lesson_id"] = lesson_id

        cursor.close()

        return redirect(
            url_for(
                "my_courses.lesson",
                course_name=formated_course_name,
                lesson_name=formated_lesson_name,
            )
        )


# This route is used to mark a lesson as completed and update the user's progress in the course
# It checks if the user has already completed the lesson and updates the database accordingly
@my_courses_bp.route("/my-courses/lesson-completed", methods=["GET", "POST"])
def lesson_completed():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        lesson_id = session.get("lesson_id")
        course_id = session.get("course_id")

        # when the user clicks on the button "Done" in the lesson page, it sends a POST request to this route
        # This route checks if the user has already completed the lesson and if not, it marks the lesson as completed
        # and updates the user's progress in the course
        # It also updates the session variables to reflect the changes made
        if request.method == "POST":
            completed = request.form.get("completed")

            if (
                completed == "completed"
            ):  # If the user has completed the lesson, check if the lesson is already marked as completed

                cursor.execute(
                    "SELECT lesson_id FROM user_lesson WHERE status ='completed' "
                )

                completed_lessons_id = cursor.fetchall()

                lesson_ids = []

                for tuple_item in completed_lessons_id:
                    for uuid in tuple_item:
                        lesson_ids.append(uuid)

                # If the lesson is not already marked as completed, insert a new record in the user_lesson table
                # This is to ensure that the user can mark the lesson as completed only once
                if lesson_id not in lesson_ids:

                    user_id = session.get("user_id")

                    import uuid

                    user_lesson_id = str(
                        uuid.uuid4()
                    )  # Generates a unique ID for the user_lesson record

                    timestamp = datetime.now().isoformat(
                        timespec="seconds"
                    )  # Gets the current timestamp in ISO format with seconds precision

                    cursor.execute(
                        "INSERT INTO user_lesson (id, lesson_id, user_id, status, completed_at) VALUES (?, ?, ?, ?, ?)",
                        (user_lesson_id, lesson_id, user_id, "completed", timestamp),
                    )

                    session["lesson_id"] = session.get("next_lesson_id")
                    conn.commit()

        cursor.execute(
            "SELECT lesson_order FROM Lesson WHERE lesson_id = ? AND course_id =?",
            (lesson_id, course_id),
        )

        current_lesson_order_number = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(lesson_order) FROM Lesson WHERE course_id = ? ",
            (course_id,),
        )

        total_number_of_lessons = cursor.fetchone()[0]

        # Update the lesson order number in the session
        # This is to ensure that the user can navigate to the next lesson after completing the current lesson
        # If the current lesson order number is less than the total number of lessons, increment the lesson order number by 1
        # Otherwise, keep the lesson order number the same
        if current_lesson_order_number < total_number_of_lessons:
            session["lesson_order"] = current_lesson_order_number + 1
        else:
            session["lesson_order"] = current_lesson_order_number

        cursor.close()

        return redirect(url_for("my_courses.intermediate_route"))

    else:
        return redirect(url_for("auth.login"))


# This route shows the lesson content for a specific course and lesson
# It retrieves the lesson content from the session and displays it on the lesson page
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
            language=session.get("language"),
            next_lesson_id=session.get("next_lesson_id"),
            prev_lesson_id=session.get("prev_lesson_id"),
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
        user_id = session.get("user_id")
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT course_id FROM Course")

        course_id_tuple = cursor.fetchall()
        completed_course_ids = []

        # This loop iterates through all the course IDs and checks if the user has completed all the lessons in that course
        # If the user has completed all the lessons, the course ID is added to the completed_course_ids list
        # This is used to display the completed courses to the user
        for element in course_id_tuple:
            for course_id in element:
                cursor.execute("""SELECT COUNT(*) FROM Lesson WHERE course_id=?""", (course_id,))
                total_number_of_lessons = cursor.fetchone()[0]

                cursor.execute("""SELECT COUNT(*) FROM user_lesson WHERE lesson_id IN (SELECT lesson_id FROM lesson WHERE course_id = ?) AND status = "completed" AND user_id=? """, (course_id,user_id,),)
                number_completed_lesson = cursor.fetchone()[0]

                if number_completed_lesson == total_number_of_lessons:
                    completed_course_ids.append(course_id)

        # This loop fetches the course data for each completed course ID
        # It retrieves the course name, language image, course image, and language from the Course table
        # The course data is then stored in the completed_courses_data list
        completed_courses_data = []

        for completed_course_id in completed_course_ids:
            cursor.execute(
                    "SELECT course_id, course_name, language_image, course_image, language FROM Course WHERE course_id=?", (completed_course_id,)
                )
            course_data = cursor.fetchall()
            for one_set_course_data in course_data:
                for data in one_set_course_data:
                    completed_courses_data.append(data)
                completed_courses_data.append(100) # Appends 100 to the list to indicate that the course is completed

        cursor.close()
        # This function divides the completed_courses_data into chunks based on the number of completed course IDs
        divided_array = divide_array_into_chunks(completed_courses_data, int(len(completed_courses_data) / len(completed_course_ids)))


        return render_template("user/my_courses/completed_courses.html", courses_data = divided_array)
    else:
        return redirect(url_for("auth.login"))


@my_courses_bp.route("/my-courses/code-editor", methods=["GET", "POST"])
def code_editor():
    if "user_id" in session:
        language = session.get("language")
        return render_template("user/my_courses/code_editor.html", language=language)
    else:
        return redirect(url_for("auth.login"))
