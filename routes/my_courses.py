from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    abort,
    jsonify,
)
import sqlite3
from datetime import datetime
import uuid
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import divide_array_into_chunks, db_execute, login_required

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

my_courses_bp = Blueprint("my_courses", __name__)


# Function to get all the courses available in the database
# I used a function to stop the repetion in the code
def get_all_courses(search_key: str = None):
    user_id = session["user_id"]
    query = """
                    SELECT
                        C.course_id,
                        C.course_name,
                        C.language_image,
                        C.course_image,
                        C.language,

                        ROUND(
                            CASE
                                WHEN (
                                    SELECT COUNT(*)
                                    FROM Lesson L2
                                    WHERE L2.course_id = C.course_id
                                ) = 0 THEN 0

                                ELSE (
                                    100.0 * (
                                        SELECT COUNT(*)
                                        FROM user_lesson UL
                                        JOIN Lesson L
                                            ON UL.lesson_id = L.lesson_id
                                        WHERE
                                            UL.user_id = ? AND
                                            UL.status = 'completed' AND
                                            L.course_id = C.course_id
                                    )
                                    /
                                    (
                                        SELECT COUNT(*)
                                        FROM Lesson L2
                                        WHERE L2.course_id = C.course_id
                                    )
                                )
                            END
                        ) AS completion_percentage

                    FROM
                        Course C
                    """
    search_query = """
                    WHERE
                        LOWER(C.course_name) LIKE ?
                    """
    if search_key is not None:
        query = query + search_query
        values = (user_id, search_key)
    else:
        values = (user_id, )

    course_data = db_execute(
        query=query, fetch=True, fetchone=False, values=values)

    if course_data:
        return course_data
    else:
        return ""

# Function to get all AI generated Courses
# I used a function to stop the repetion in the code


def get_ai_courses(user_id):
    query = """
            SELECT
                resource_id,
                title,
                status,
                SUBSTR(generated_at, 1, instr(generated_at, 'T') - 1)
                    AS generated_date
            FROM
                Ai_resource
            WHERE user_id  = ?
        """

    ai_courses_data_form_db = db_execute(
        query=query, fetch=True, fetchone=False, values=(user_id,))

    if ai_courses_data_form_db:
        return ai_courses_data_form_db
    else:
        return "null"

# This route is used to display all the courses available in the application


@my_courses_bp.route("/my-courses", methods=["GET", "POST"])
@login_required
def all_courses():
    courses_data = get_all_courses()

    if request.method == "POST":
        course_id = request.form.get("course_id")

        course_id_tuple = db_execute(
            query="SELECT course_id FROM Course WHERE course_id = ?",
            fetch=True,
            fetchone=False,
            values=(course_id,))

        if course_id_tuple:
            session["course_id"] = course_id
        else:
            abort(404)

        user_id = session.get("user_id")
        enrollment_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat(timespec="seconds")

        insert_query = """
            INSERT INTO Enrollment (
                enrollment_id,
                user_id,
                course_id,
                enrolled_at,
                status,
                last_accessed
            )
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM Enrollment
                WHERE user_id = ? AND course_id = ?
            )
        """

        db_execute(
            query=insert_query,
            fetch=False,
            fetchone=False,
            values=(
                enrollment_id,
                user_id,
                course_id,
                timestamp,
                "started",
                timestamp,
                user_id,
                course_id
            )
        )

        update_query = """
            UPDATE Enrollment
            SET last_accessed = ?
            WHERE user_id = ? AND course_id = ? AND status = 'started'
            """

        db_execute(query=update_query, fetch=False, fetchone=False,
                   values=(timestamp, user_id, course_id))

        session["lesson_order"] = 1

        return redirect(url_for("my_courses.intermediate_route"))

    return render_template(
        "user/my_courses/all-courses.html", courses_data=courses_data
    )


# This route is used to search for courses based on a keyword entered by
# the user
@my_courses_bp.route("/my-courses/search", methods=["GET"])
@login_required
def search_courses():
    if request.method == "GET":
        keyword = request.args.get(
            "search"
            # Gets the keyword entered by the user and converts it to
            # lowercase for case-insensitive search
        ).lower()
        if not keyword == "" and not keyword.isspace():
            search_term = f"%{keyword.lower()}%"

            course_data = get_all_courses(search_term)

            # Uses the same variable name as the original route to reduce
            # the repetition of code in the template
            return render_template(
                "user/my_courses/search-result-all-courses.html",
                courses_data=course_data,
            )
        else:
            return redirect(url_for("my_courses.all_courses"))

# This route is to process all the lesson data and
# works as an intermediate route
# between the all_courses route and the lesson route.
# It fetches the lesson data from the database and stores it in the
# session for later use


@my_courses_bp.route("/my-courses/intermediate", methods=["POST", "GET"])
def intermediate_route():
    if "user_id" in session:
        course_id = session.get("course_id")
        # If the request method is POST, it means the user has selected a
        # lesson
        if request.method == "POST":
            lesson_id = request.form.get("lesson_id")
            session["lesson_id"] = lesson_id

        #    Lesson_id              Lesson_id
        #   (My course)           (Dashboard)
        #      │                       │
        #      │                       │
        #      └──────────►    ◄───────┘
        #             session lesson_id
        #                   │
        #                   │
        #                   ▼
        #              Validation

        # If the lesson_id is null
        # gets the lesson_id that suit to the lesson_order numner
        lesson_id = session.get('lesson_id')
        lesson_order = session.get('lesson_order')
        lesson_id_query = """
            SELECT
                COALESCE
                (
                (SELECT L1.lesson_id FROM Lesson L1
                    WHERE L1.lesson_id = :lid AND L1.course_id = :cid),
                (SELECT L2.lesson_id FROM Lesson L2
                    WHERE L2.lesson_order = :lnu AND L2.course_id=:cid)
                )
            AS lesson_id
            """

        lesson_id = db_execute(query=lesson_id_query,
                               fetch=True,
                               fetchone=True,
                               values={
                                   "lid": lesson_id,
                                   "cid": course_id,
                                   "lnu": lesson_order
                               }
                               )

        if lesson_id:
            lesson_id = lesson_id[0]
        else:
            abort(404)

        session["lesson_id"] = lesson_id

        course_descriptor_query = """
                                SELECT
                                    language,
                                    course_name,
                                    (
                                    SELECT lesson_title
                                    FROM Lesson as L
                                    WHERE L.lesson_id = :lid
                                        AND L.course_id = :cid
                                    ) as lesson_title
                                FROM
                                    Course as C
                                WHERE
                                    C.course_id = :cid
                                """

        course_descriptor = db_execute(query=course_descriptor_query,
                                       fetch=True,
                                       fetchone=False,
                                       values={
                                           "lid": lesson_id,
                                           "cid": course_id
                                       }
                                       )

        session['language'] = course_descriptor[0][0]

        course_name = course_descriptor[0][1]

        lesson_title = course_descriptor[0][2]

        # Formats the course name by replacing spaces with hyphens for URL
        # compatibility
        formated_course_name = "-".join(course_name.split(" "))

        # Formats the lesson name by replacing spaces with hyphens for URL
        # compatibility
        formated_lesson_name = "-".join(lesson_title.split(" "))

        return redirect(
            url_for(
                "my_courses.lesson",
                course_name=formated_course_name,
                lesson_name=formated_lesson_name,
            )
        )
    else:
        return redirect(url_for("auth.login"))


# This route is used to mark a lesson as completed and
# update the user's progress in the course
# It checks if the user has already completed the lesson and updates the
# database accordingly
@my_courses_bp.route("/my-courses/lesson-completed", methods=['POST'])
def lesson_completed():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    complete_request = request.form.get("completed")

    if complete_request == "completed":

        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        lesson_id = session.get("lesson_id")
        course_id = session.get("course_id")
        user_id = session.get("user_id")

        user_lesson_id = str(
            uuid.uuid4()
        )  # Generates a unique ID for the user_lesson record

        # Gets the current timestamp in ISO format with seconds
        # precision
        timestamp = datetime.now().isoformat(timespec="seconds")

        insert_query = """
                INSERT INTO
                user_lesson (id,
                            lesson_id,
                            user_id,
                            status,
                            completed_at)
                SELECT :id, :lid, :uid, :status, :completed_at
                WHERE NOT EXISTS (
                    SELECT 1 FROM user_lesson
                    WHERE status = 'completed'
                    AND lesson_id = :lid
                    AND user_id = :uid
                );"""

        update_query = """
                UPDATE Enrollment
                SET status = 'completed',
                    completed_at = :completed_at
                WHERE user_id = :uid
                AND course_id = :cid
                AND status != 'completed'
                AND (
                    SELECT COUNT(*) FROM Lesson
                    WHERE course_id = :cid
                ) = (
                    SELECT COUNT(*) FROM User_lesson
                    WHERE user_id = :uid
                    AND lesson_id IN (
                        SELECT lesson_id FROM Lesson WHERE course_id = :cid
                    )
                );
            """

        db_execute(query=insert_query + update_query,
                   fetch=False,
                   fetchone=False,
                   values={"id": user_lesson_id,
                           "lid": lesson_id,
                           "uid": user_id,
                           "status": "completed",
                           "completed_at": timestamp,
                           "cid": course_id
                           })

        session["lesson_id"] = session.get("next_lesson_id")

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


# This route shows the lesson content for a specific course and lesson
# It retrieves the lesson content from the session and displays it on the
# lesson page
@my_courses_bp.route("/my-courses/<course_name>/<lesson_name>",
                     methods=["GET", "POST"])
def lesson(course_name, lesson_name):
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        course_id = session.get("course_id")

        lesson_id = session.get("lesson_id")
        user_id = session.get("user_id")

        cursor.execute(
            """
                SELECT
                (
                    SELECT c.course_name
                    FROM course AS c
                    WHERE c.course_id = :cid
                ) AS course_name,
                l.lesson_id,
                l.lesson_title,
                l.content,

                /* Calculate the percentage of completion in the course */
                ROUND(
                    100
                    * (
                    SELECT COUNT(*)
                    FROM user_lesson AS ul
                    WHERE
                        ul.user_id = :uid
                        AND ul.lesson_id IN
                        (
                        SELECT l9.lesson_id
                        FROM
                            lesson AS l9
                        WHERE l9.course_id = :cid
                        )
                        AND
                        ul.status = "completed"
                    ) / (
                    SELECT COUNT(*)
                    FROM lesson AS l2
                    WHERE l2.course_id = :cid
                    )
                ) AS percentage,

                -- Get the "next" lesson's ID (or the last if already at the end)
                (
                    SELECT l4.lesson_id
                    FROM lesson AS l4
                    WHERE
                    l4.course_id = :cid
                    AND l4.lesson_order
                    = CASE
                        WHEN
                        l.lesson_order + 1 > (
                            SELECT COUNT(*)
                            FROM lesson AS l5
                            WHERE l5.course_id = :cid
                        )
                        THEN (
                            SELECT COUNT(*)
                            FROM lesson AS l5
                            WHERE l5.course_id = :cid
                        )
                        ELSE l.lesson_order + 1
                    END
                    LIMIT 1
                ) AS next_lesson_id,

                -- Get the "prev" lesson's ID (or the first if already at the first)
                (
                    SELECT l6.lesson_id
                    FROM lesson AS l6
                    WHERE
                    l6.course_id = :cid
                    AND l6.lesson_order
                    = CASE
                        WHEN l.lesson_order - 1 != 0
                        THEN l.lesson_order - 1
                        ELSE l.lesson_order
                    END
                    LIMIT 1
                ) AS prev_lesson_id,

                -- Get all the lesson titles with relevant ids in the course
                (
                    SELECT
                      GROUP_CONCAT("[" || l7.lesson_id || "," || l7.lesson_title || "]", ", ")
                    FROM
                    lesson AS l7
                    WHERE
                    l7.course_id = :cid
                ) AS all_lessons_list
                FROM
                lesson AS l
                WHERE
                l.course_id = :cid
                AND
                l.lesson_id = :lid

            """, {"cid": course_id, "lid": lesson_id, "uid": user_id})

        lesson_page_data = cursor.fetchall()
        cursor.close()

        if lesson_page_data:
            # Gets the lessons list with its ids from the database
            # removes outer brackets [1:-1]
            # then replaces ("], [") with commas to make a flat array
            raw_data = lesson_page_data[0][7][1:-1].replace("], [", ",")
            flat_array = raw_data.split(",")

            # Converts the flat array into a 2d array
            lessons_data = divide_array_into_chunks(flat_array, 2)

            return render_template(
                "user/my_courses/lesson.html",
                lesson_page_data=lesson_page_data[0],
                lessons_data=lessons_data
            )
        else:
            return 404

    else:
        return redirect(url_for("auth.login"))


# This route is used to display the courses that the user has completed
@my_courses_bp.route("/my-courses/completed-courses", methods=["GET", "POST"])
def completed_courses():
    if "user_id" in session:
        user_id = session.get("user_id")
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT
                    C.*,
                    100.0 AS percentage
                FROM Course C
                WHERE C.course_id IN
                (SELECT E.course_id
                FROM Enrollment E
                WHERE E.user_id = ?
                AND E.status = 'completed')
        """, (user_id,))
        completed_courses_data = cursor.fetchall()
        if completed_courses_data:
            return render_template(
                "user/my_courses/completed-courses.html",
                courses_data=completed_courses_data)
        else:
            return render_template(
                "user/my_courses/completed-courses.html")
    else:
        return redirect(url_for("auth.login"))


# This route is used to display the code editor for the user to write and test their code
# It checks if the user is logged in and retrieves the programming language from the session
# language is used for to set language in the code editor
@my_courses_bp.route("/my-courses/code-editor", methods=["GET", "POST"])
def code_editor():
    if "user_id" in session:
        language = session.get("language")
        return render_template(
            "user/my_courses/code-editor.html", language=language)
    else:
        return redirect(url_for("auth.login"))


# This route is used to display the AI-generated courses that the user has
# created
@my_courses_bp.route("/my-courses/ai_generated", methods=["GET", "POST"])
def ai_courses():
    if "user_id" in session:
        user_id = session.get("user_id")
        ai_courses_data = get_ai_courses(user_id)

        return render_template(
            "user/my_courses/ai-generated-courses.html",
            ai_courses_data=ai_courses_data)
    else:
        return redirect(url_for("auth.login"))


# This route is used to generate a course based on the user's input using AI
# It checks if the user is logged in and if the request is a POST request
# with JSON
@my_courses_bp.route("/my-courses/ai_generated/generating", methods=["POST"])
def generarting_course():
    if "user_id" in session:
        if request.is_json and request.method == "POST":
            data = request.get_json()
            user_input = data.get("userInput")

            if user_input.strip():
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are an AI assistant integrated into the Ada Learning Platform, developed by G. A. Pasindu Vidunitha. Your role is to generate a simple, clear, and suitable course name based on the following user input: {user_input}.Return only the course name as plain text. Do not include any labels, prefixes, or extra text (e.g., avoid phrases like "Course name:", "Here is your course:", etc.). Output only the name itself.If the user input is random, unclear, or does not make sense, generate a meaningful beginner-friendly course name on your own and proceed accordingly.""",
                        },
                        {
                            "role": "user",
                            "content": user_input,
                        },
                    ],
                    temperature=1,
                    top_p=1,
                    model=model,
                )

                course_name = response.choices[0].message.content

                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "",
                        },
                        {
                            "role": "user",
                            "content": f"You are an AI assistant integrated into the Ada Learning Platform, developed by G. A. Pasindu Vidunitha. Ada is a platform designed to help beginner developers learn programming and software development effectively.Your role is to generate beginner-friendly, easy-to-understand course content based on the following user input: {course_name}.Use proper HTML tags for all content, including headings (<h2>), paragraphs (<p>), lists (<ul>, <li>), and code blocks (<pre><code>). This ensures the output can be rendered cleanly in a webpage. Do not include introductions, explanations, or phrases like “Here is your course” — just return the raw structured HTML content. If the user input is random, unclear, or does not make sense, generate a meaningful beginner-friendly course topic on your own and proceed accordingly.",
                        },
                    ],
                    temperature=1,
                    top_p=1,
                    model=model,
                )

                course_content = response.choices[0].message.content

                conn = sqlite3.connect("database/app.db")
                cursor = conn.cursor()

                user_id = session.get("user_id")

                resource_id = str(uuid.uuid4())

                timestamp = datetime.now().isoformat(timespec="seconds")

                cursor.execute(
                    """
                    INSERT INTO Ai_resource
                        (resource_id,
                        user_id,
                        title,
                        content,
                        generated_at,
                        status)
                    VALUES (?, ?, ?, ?, ?, ?)
                            """,
                    (
                        resource_id,
                        user_id,
                        course_name,
                        course_content,
                        timestamp,
                        "Haven't Done",
                    ),
                )
                conn.commit()

                conn.close()

                ai_courses_url = url_for("my_courses.ai_courses")
                return (
                    jsonify({"redirect_url": ai_courses_url,
                            "status": "created"}),
                    200,
                )
            else:
                return jsonify({"error": "Invalid Input"})

        else:
            return jsonify({"error": "Invalid JSON"}), 400
    else:
        return redirect(url_for("auth.login"))


# This route is used to search for AI-generated courses based on a keyword entered by the user
# It checks if the user is logged in and retrieves the AI courses data
# from the session
@my_courses_bp.route("/my-courses/ai_generated/search",
                     methods=["POST", "GET"])
def search_ai_courses():
    if "user_id" in session:
        user_id = session.get("user_id")
        if request.method == "GET":
            keyword = request.args.get("search")
            if not keyword == "" and not keyword.isspace():
                conn = sqlite3.connect("database/app.db")
                cursor = conn.cursor()
                search_term = f"%{keyword.lower()}%"
                cursor.execute(
                    """
                        SELECT
                            resource_id,
                            title,
                            status,
                            SUBSTR(generated_at, 1, instr(generated_at, 'T') - 1) AS generated_date
                        FROM
                            Ai_resource
                        WHERE user_id  = ?
                            AND
                            LOWER(title) LIKE ?
                    """, (user_id, search_term))
                searched_ai_courses_data = cursor.fetchall()
                return render_template(
                    "user/my_courses/search-ai-courses.html",
                    ai_courses_data=searched_ai_courses_data,
                )
            else:
                return redirect(url_for("my_courses.ai_courses"))
    else:
        return redirect(url_for("auth.login"))


# This route is used to handle the intermediate step when showing all AI-generated courses
# This works between the AI-generated courses page and the AI course content page
# It checks if the user is logged in and retrieves the AI resource ID from
# the form submission
@my_courses_bp.route("/my-courses/ai_generated/intermediate",
                     methods=["POST", "GET"])
def intermediate_route_ai():
    if "user_id" in session:
        if request.method == "POST":

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            user_id = session.get("user_id")

            ai_resource_id = request.form.get("ai-course-id")

            cursor.execute(
                "SELECT title FROM Ai_resource WHERE resource_id =? and user_id=?",
                (ai_resource_id,
                 user_id,
                 ),
            )
            row = cursor.fetchone()

            conn.close()

            # If the AI resource ID is not found, return a 404 error
            # This is to ensure that the user cannot access a course that does
            # not exist
            if not row:
                abort(404)

            course_name = row[0]

            session["ai_courses_id"] = ai_resource_id

            formated_course_name = "-".join(course_name.split(" "))

            return redirect(
                url_for(
                    "my_courses.ai_course",
                    course_name=formated_course_name)
            )

    else:
        return redirect(url_for("auth.login"))


# This route is used to display the AI-generated course content
@my_courses_bp.route("/my-courses/ai_generated/<course_name>")
def ai_course(course_name):
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        user_id = session.get("user_id")
        ai_resource_id = session.get("ai_courses_id")

        cursor.execute(
            "SELECT title, content FROM Ai_resource WHERE resource_id =? and user_id=?",
            (ai_resource_id,
             user_id,
             ),
        )
        ai_course_data = cursor.fetchall()[0]
        conn.close()
        title = ai_course_data[0]
        content = ai_course_data[1]

        session["ai_course_topic"] = title

        return render_template(
            "user/my_courses/ai-course.html",
            content=content,
            course_name=title)
    else:
        return redirect(url_for("auth.login"))


# This route is used to mark an AI-generated course as completed
# It checks if the user is logged in and updates the course status in the
# database
@my_courses_bp.route("/my-courses/ai_generated/completed", methods=["POST"])
def ai_course_complete():
    if "user_id" in session:
        if request.method == "POST":
            completed = request.form.get("completed")
            if completed == "completed":
                ai_resource_id = session.get("ai_courses_id")
                user_id = session.get("user_id")
                conn = sqlite3.connect("database/app.db")
                cursor = conn.cursor()

                cursor.execute(
                    """
                        UPDATE Ai_resource
                        SET status = 'Completed'
                        WHERE resource_id = ?
                        AND user_id = ?
                        AND status != 'Completed'
                    """, (ai_resource_id, user_id))

                conn.commit()
                cursor.close()

        return redirect(url_for("my_courses.ai_courses"))
    else:
        return redirect(url_for("auth.login"))
