"""
Handles all the routes in My course section
"""

import os
from datetime import datetime
import uuid
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
from openai import OpenAI
from dotenv import load_dotenv
from ai_chat import ai_response
from utils import divide_array_into_chunks, db_execute, login_required

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=token,
)

my_courses_bp = Blueprint("my_courses", __name__)


# Function to get all the courses available in the database
# I used a function to stop the repetion in the code
def get_all_courses(search_key: str = None):
    """
    This function gets all courses and each course's completion percentage
    for the logged-in user.

    The function reads the user_id from the session and runs a SQL query
    that returns the course id, name, images, language, and
    a rounded completion percentage based on how many lessons the user
    has completed in each course. If a search key is provided,
    it filters courses by name (case-insensitive).
    It returns the full list of matching courses with their details;
    if none are found, it returns an empty string.

    Args:
        search_key (str, optional): Text to filter courses by name.
        Defaults to None.

    Returns:
        list | str: A list of course rows with details and
        completion percentage, or an empty string if no data.
    """
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
def get_ai_courses(search_key: str = None):
    """
    This function gets all the AI generated courses for the logged-in user.

    The function reads the user_id from the session and
    queries the Ai_resource table for the course id, title, status,
    and the generated date. If a search key is provided,
    it filters the results by title in a case-insensitive way.
    It returns all matching AI generated courses from the database,
    or "null" if no data is found.

    Args:
        search_key (str, optional): Text to filter courses by title.
        Defaults to None.

    Returns:
        list | str: A list of AI generated courses with details,
        or "null" if no data.
    """
    user_id = session["user_id"]
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

    search_query = """
                    AND
                    LOWER(title) LIKE ?
                    """
    if search_key is not None:
        query = query + search_query
        values = (user_id, search_key)
    else:
        values = (user_id, )

    ai_courses_data_form_db = db_execute(
        query=query, fetch=True, fetchone=False, values=values)

    if ai_courses_data_form_db:
        return ai_courses_data_form_db
    else:
        return "null"


# This route is used to display all the courses available in the application
@my_courses_bp.route("/my-courses", methods=["GET", "POST"])
@login_required
def all_courses():
    """
    This route shows all available courses and handles enrolling into a course.

    The function loads all courses using get_all_courses() and, on GET,
    renders the courses page. On POST, it reads the selected course_id,
    checks that it exists, and saves it to the session. It then creates
    an enrollment record if one does not already exist for this user and
    course (using a UUID and an ISO timestamp), updates last_accessed for
    the started course, sets the initial lesson_order in
    the session, and redirects to the intermediate route.
    If the course_id is invalid, it returns a 404 error.


    Returns:
        - Rendered HTML with all courses (GET) or a redirect to the
        intermediate route after enrollment (POST).
    """
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
    """
    This route searches for courses based on the keyword entered by the user.

    The function gets the search keyword from the request arguments
    and converts it to lowercase for case-insensitive matching.
    If the keyword is valid, it creates a search term,
    calls get_all_courses() with it, and renders the search-result
    template with the results. If the keyword is empty or only spaces,
    it redirects the user back to the all courses page.


    Returns:
        Response: Rendered HTML template with the search results, or a redirect
        to the all courses page if the keyword is invalid.
    """
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
@login_required
def intermediate_route():
    """
    This route processes lesson data and works as an intermediate step
    between the all_courses route and the lesson route.

    The function gets the course_id and lesson_id from the session or the
    form (if POST). If lesson_id is missing, it validates and sets it
    using the lesson_order number. It then queries the database for the
    course language, course name, and lesson title. These values are saved
    in the session and formatted with hyphens for URL compatibility.
    Finally, it redirects the user to the lesson route with the formatted
    course and lesson names.


    Returns:
        - Redirect to the lesson route with formatted course and
        lesson names.
    """
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


# This route is used to mark a lesson as completed and
# update the user's progress in the course
# It checks if the user has already completed the lesson and updates the
# database accordingly
@my_courses_bp.route("/my-courses/lesson-completed", methods=['POST'])
@login_required
def lesson_completed():
    """
    This route marks a lesson as completed and updates the user's course
    progress.

    The function checks the form input for "completed". If valid, it gets
    the lesson_id, course_id, and user_id from the session. It inserts a
    record into the user_lesson table if the lesson is not already marked
    as completed, and updates the Enrollment table to completed if all
    lessons in the course are done. It then updates the session with the
    next lesson_id and lesson order so the user can continue smoothly.
    Finally, it redirects to the intermediate route.


    Returns:
        Response: Redirect to the intermediate route after progress is
        updated.
    """
    complete_request = request.form.get("completed")
    if complete_request == "completed":
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

        db_execute(query=insert_query,
                   fetch=False,
                   fetchone=False,
                   values={"id": user_lesson_id,
                           "lid": lesson_id,
                           "uid": user_id,
                           "status": "completed",
                           "completed_at": timestamp,
                           "cid": course_id
                           })

        db_execute(query=update_query,
                   fetch=False,
                   fetchone=False,
                   values={"uid": user_id,
                           "status": "completed",
                           "completed_at": timestamp,
                           "cid": course_id
                           })

        session["lesson_id"] = session.get("next_lesson_id")

        # Update the lesson order number in the session
        # This is to ensure that the user can navigate to the next lesson
        # after completing the current lesson
        # If the current lesson order number is less than
        # the total number of lessons increment the lesson order number by 1
        # Otherwise, keep the lesson order number the same
        # I done this, because if the new lesson id is not in the database
        # Program can use the this lesson id

        new_lesson_order_number_query = """
                    WITH cur AS (
                    SELECT lesson_order
                    FROM Lesson
                    WHERE course_id = :cid AND lesson_id = :lid
                    )
                    SELECT CASE
                            WHEN (
                                    SELECT COUNT(*)
                                    FROM Lesson
                                    WHERE course_id = :cid) > cur.lesson_order
                            THEN cur.lesson_order + 1
                            ELSE cur.lesson_order
                        END AS next_lesson_order
                    FROM cur;
                    """

        new_lesson_order_number = db_execute(
            query=new_lesson_order_number_query,
            fetch=True,
            fetchone=True,
            values={"cid": course_id,
                    "lid": lesson_id})

        session["lesson_order"] = new_lesson_order_number[0]
        return redirect(url_for("my_courses.intermediate_route"))


# This route shows the lesson content for a specific course and lesson
# It retrieves the lesson content from the session and displays it on the
# lesson page
@my_courses_bp.route("/my-courses/<course_name>/<lesson_name>")
@login_required
def lesson(_course_name, _lesson_name):
    """
    This route shows the lesson content for a specific course and lesson.

    The function gets the course_id, lesson_id, and user_id from the
    session. It runs a query to load the lesson title, content,
    completion percentage, navigation ids for next and previous lessons,
    and a list of all lessons in the course. The data is processed to
    create a clean 2D array of lesson ids and titles. Finally, the
    lesson.html template is rendered with the lesson data. If no data is
    found, it returns a 404 error.

    Args:
        course_name (str): The course name from the URL (not used in the
        function logic).
        lesson_name (str): The lesson name from the URL (not used in the
        function logic).

    Returns:
        - Rendered HTML template with the lesson data, or a 404
        error if no lesson is found.
    """
    course_id = session.get("course_id")
    lesson_id = session.get("lesson_id")
    user_id = session.get("user_id")

    lesson_pg_query = """
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

            -- Get the "prev" lesson's ID
            -- (or the first if already at the first)
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
                    GROUP_CONCAT(
                    "[" || l7.lesson_id || "," || l7.lesson_title || "]", ", ")
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

        """

    lesson_page_data = db_execute(query=lesson_pg_query,
                                  fetch=True,
                                  values={"cid": course_id,
                                          "lid": lesson_id,
                                          "uid": user_id})

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


# This route is used to display the courses that the user has completed
@my_courses_bp.route("/my-courses/completed-courses")
@login_required
def completed_courses():
    """
    This route shows all courses that the logged-in user has completed.

    The function gets the user_id from the session and queries the
    database for all courses marked as completed in the Enrollment
    table. Each completed course is returned with a 100% completion
    rate. If data is found, it renders the completed-courses.html
    template with the courses; otherwise, it renders the same
    template with no data.


    Returns:
        - Rendered HTML template with the completed courses or
        an empty template if no completed courses exist.
    """
    user_id = session.get("user_id")
    query = """
            SELECT
                C.*,
                100.0 AS percentage
            FROM Course C
            WHERE C.course_id IN
            (SELECT E.course_id
            FROM Enrollment E
            WHERE E.user_id = ?
            AND E.status = 'completed')
    """
    completed_courses_data = db_execute(query=query,
                                        fetch=True,
                                        values=(user_id,))
    if completed_courses_data:
        return render_template(
            "user/my_courses/completed-courses.html",
            courses_data=completed_courses_data)
    else:
        return render_template(
            "user/my_courses/completed-courses.html")


# This route is used to display the code editor
# for the user to write and test their code
# It checks if the user is logged in and
# retrieves the programming language from the session
# language is used for to set language in the code editor
@my_courses_bp.route("/my-courses/code-editor")
@login_required
def code_editor():
    """
    This route shows the code editor for the logged-in user.

    The function gets the programming language from the session and uses
    it to set the editor's language. It then renders the code-editor.html
    template with the selected language.


    Returns:
        - Rendered HTML template with the code editor.
    """
    language = session.get("language")
    return render_template(
        "user/my_courses/code-editor.html", language=language)


# This route is used to display the AI-generated courses that the user has
# created
@my_courses_bp.route("/my-courses/ai_generated")
@login_required
def ai_courses():
    """
    This route shows all AI-generated courses created by the logged-in
    user.

    The function calls get_ai_courses() to fetch the list of AI-generated
    courses for the current user. It then renders the ai-generated-courses.html
    template with the course data.


    Returns:
        Response: Rendered HTML template with the AI-generated courses.
    """
    ai_courses_data = get_ai_courses()

    return render_template(
        "user/my_courses/ai-generated-courses.html",
        ai_courses_data=ai_courses_data)


# This route is used to generate a course based on the user's input using AI
# It checks if the user is logged in and if the request is a POST request
# with JSON
@my_courses_bp.route("/my-courses/ai_generated/generating", methods=["POST"])
@login_required
def generarting_course():
    """
    This route generates an AI course based on the user's input.

    The function reads JSON data from the POST request and gets the
    userInput field. It sends the input to the AI model to generate a
    simple and clear course name. If the name is invalid, it returns
    an error message. If valid, it sends another request to the AI model
    to generate the full beginner-friendly course content in HTML format.
    The course name and content are saved in the Ai_resource table with
    a timestamp and default status. Finally, it returns a JSON response
    with a redirect URL to the AI courses page and a status of "created".


    Returns:
        Response: JSON object with either an error or the redirect URL
        after the course is generated and saved.
    """
    data = request.get_json()
    user_input = data.get("userInput")

    if user_input.strip():
        system_content = f"""
                            You are an AI assistant integrated into
                            the Ada Learning Platform, developed by
                            G. A. Pasindu Vidunitha.
                            Your role is to generate a simple, clear,
                            and suitable course name based on the
                            following user input: {user_input}.
                            Return only the course name as plain text.
                            Do not include any labels, prefixes,
                            or extra text
                            (e.g., avoid phrases like "Course name:",
                            "Here is your course:", etc.).
                            Output only the name itself.
                            If the user input is random, unclear, or
                            not related to programming or related
                            fields (e.g., software, data, AI/ML, IT,
                            cybersecurity), output exactly "invalid"
                            and nothing else.
                            """

        ai_response_result = ai_response(system_content=system_content,
                                         user_input=user_input)

        if ai_response_result["error"]:
            return jsonify(
                {"error": ai_response_result['error']})

        course_name = ai_response_result['result']

        if course_name == "invalid":
            return jsonify(
                {"error": "Invalid topic. Enter a programming-related subject."
                 })

        system_content_for_course_generating = f"""
                    You are an AI assistant integrated into
                    the Ada Learning Platform, developed by
                    G. A. Pasindu Vidunitha. Ada is a platform
                    designed to help beginner developers
                    learn programming and software development
                    effectively.Your role is to generate beginner-friendly,
                    easy-to-understand course content based on
                    the following user input: {course_name}.
                    Use proper HTML tags for all content,
                    including headings (<h2>), paragraphs (<p>),
                    lists (<ul>, <li>), and code blocks (<pre><code>).
                    This ensures the output can be rendered cleanly
                    in a webpage.Do not include introductions,
                    explanations,or phrases like “Here is your course” —
                    just return the raw structured HTML content.
                    If the user input is random, unclear,
                    or does not make sense,generate a
                    meaningful beginner-friendly course
                    topic on your own and proceed accordingly."""

        course_ai_response = ai_response(
            system_content=system_content_for_course_generating,
            user_input=course_name)

        if course_ai_response["error"]:
            return jsonify(
                {"error": course_ai_response["error"]})

        course_content = course_ai_response["result"]

        user_id = session.get("user_id")

        resource_id = str(uuid.uuid4())

        timestamp = datetime.now().isoformat(timespec="seconds")

        insert_query = """
            INSERT INTO Ai_resource
                (resource_id,
                user_id,
                title,
                content,
                generated_at,
                status)
            VALUES (?, ?, ?, ?, ?, ?)
                    """

        db_execute(query=insert_query,
                   fetch=False,
                   values=(
                       resource_id,
                       user_id,
                       course_name,
                       course_content,
                       timestamp,
                       "Haven't Done",
                   ))

        ai_courses_url = url_for("my_courses.ai_courses")
        return (
            jsonify({"redirect_url": ai_courses_url,
                    "status": "created"}),
            200,
        )
    else:
        return jsonify({"error": "Invalid Input"})


# This route is used to search for AI-generated courses based
# on a keyword entered by the user
# It checks if the user is logged in and retrieves the AI courses data
# from the session
@my_courses_bp.route("/my-courses/ai_generated/search",
                     methods=["GET"])
@login_required
def search_ai_courses():
    """
    This route searches for AI-generated courses by a keyword entered by
    the user.

    The function gets the search keyword from the request arguments and
    checks that it is not empty or only spaces. If valid, it builds a
    search term, calls get_ai_courses() with it, and renders the
    search-ai-courses.html template with the results.


    Returns:
        - Rendered HTML template with the search results for AI
        courses.
    """
    keyword = request.args.get("search")
    if not keyword == "" and not keyword.isspace():
        search_term = f"%{keyword.lower()}%"
        searched_ai_courses_data = get_ai_courses(search_term)
        return render_template(
            "user/my_courses/search-ai-courses.html",
            ai_courses_data=searched_ai_courses_data,
        )


# This route is used to handle the intermediate step
# when showing all AI-generated courses
# This works between the AI-generated courses page
# and the AI course content page
# It checks if the user is logged in and retrieves the AI resource ID from
# the form submission
@my_courses_bp.route("/my-courses/ai_generated/intermediate",
                     methods=["POST"])
@login_required
def intermediate_route_ai():
    """
    This route handles the intermediate step when opening an AI-generated
    course.

    The function gets the ai-course-id from the form and checks if it exists
    in the Ai_resource table for the logged-in user. If the id is valid, it
    saves it to the session, formats the course name with hyphens, and then
    redirects to the ai_course route. If the id does not exist, it returns a
    404 error.


    Returns:
        Response: Redirect to the ai_course page if valid, otherwise a 404
        error.
    """
    user_id = session.get("user_id")

    ai_resource_id = request.form.get("ai-course-id")

    query = """
        SELECT title
        FROM Ai_resource
        WHERE resource_id =? and user_id=?"""

    row = db_execute(query=query,
                     fetch=True,
                     fetchone=True,
                     values=(ai_resource_id,
                             user_id,
                             ))

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


# This route is used to display the AI-generated course content
@my_courses_bp.route("/my-courses/ai_generated/<course_name>")
@login_required
def ai_course(_course_name):
    """
    This route shows the content of an AI-generated course.

    The function gets the user_id and ai_resource_id from the session and
    queries the ai_resource table to load the course title and content.
    It saves the title in the session as the current topic and
    then renders the ai-course.html template
    with the course content and name.

    Args:
        course_name (str): The name of the course from the URL
        (used only for routing).

    Returns:
        - Rendered HTML template showing the AI-generated
        course content.
    """
    user_id = session.get("user_id")
    ai_resource_id = session.get("ai_courses_id")

    query = """
        select
            title,
            content
        from ai_resource
        where resource_id =?
            and user_id=?"""

    ai_course_data = db_execute(query=query,
                                fetch=True,
                                values=(ai_resource_id,
                                        user_id,
                                        ))[0]
    title = ai_course_data[0]
    content = ai_course_data[1]

    session["ai_course_topic"] = title

    return render_template(
        "user/my_courses/ai-course.html",
        content=content,
        course_name=title)


# This route is used to mark an AI-generated course as completed
# It checks if the user is logged in and updates the course status in the
# database
@my_courses_bp.route("/my-courses/ai_generated/completed", methods=["POST"])
@login_required
def ai_course_complete():
    """
    This route marks an AI-generated course as completed.

    The function checks the form input for the word "completed". If it matches,
    it gets the course id from the session and the user_id from the session,
    then updates the Ai_resource table to set the status as 'Completed'
    for that course if it is not already marked. Finally,
    it redirects the user back to the AI courses page.


    Returns:
        - Redirect to the AI courses page after
        marking the course as completed.
    """
    completed = request.form.get("completed")
    if completed == "completed":
        ai_resource_id = session.get("ai_courses_id")
        user_id = session.get("user_id")

        update_query = """
                UPDATE Ai_resource
                SET status = 'Completed'
                WHERE resource_id = ?
                AND user_id = ?
                AND status != 'Completed'
            """

        db_execute(query=update_query,
                   fetch=False,
                   values=(ai_resource_id, user_id))

        return redirect(url_for("my_courses.ai_courses"))
