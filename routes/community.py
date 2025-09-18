"""
Handles all the routes and fucntions related to Community section
"""

from datetime import datetime
import uuid
import string
from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    request,
    jsonify,
    render_template,
)
import strip_markdown
import markdown
import emoji
from utils import db_execute, login_required, check_characters_limit

community_bp = Blueprint("community", __name__)


# All routes check if the user logged in or not
# If the user is not logged in, it redirects to the login page


# I Use a function because I can use this function to get all community
# questions and filter them according to the below routes
def get_community_questions_from_db(filter_query: str, since_id: str):
    """
    Function to get all the questions that are asked by users.

    It takes the user_id from the session variables,
        and creates a static base
        (This is for the images that are not starting from "https").
        This function gets the last ID through the parameter called 'since_id'.
        This is due to the current system using the polling method
        to keep updating the page; therefore,
        the program wants the last ID (since_id) to get the last time
        that fetch happened. It can be empty.
    Questions that are done by the login user will change to
        “You” instead of the full own name
    Questions that happen during the current date show only the time

    Args:
        - filter_query (string): for searching and other filtering purposes
        - since_id (string): last ID of the previous fetch

    Returns:
        - An array: Includes question_id, question with no markdown codes,
                    created time, person who asked the question,
                    profile image url, number of answers, and save status
        - or a string: "" (if there are no questions)
    """
    user_id = session.get("user_id")

    # Creates a URL for this static base for profile images
    # In the SQL query,
    #   if the image location does not start from
    #   'https', it will use this + image file name
    static_base = url_for('static', filename='')

    # ts: time stamp
    since_ts_query = """
                SELECT
                    created_at
                FROM Question
                WHERE question_id = ?
                """
    since_ts = db_execute(query=since_ts_query,
                          fetch=True,
                          fetchone=True,
                          values=(since_id, ))

    # The above fetch's result is a tuple,
    # and to run the SQL query without crashing
    # make it an empty array
    if not since_ts:
        since_ts = [""]

    base_query = """
            SELECT
                Q.question_id,
                Q.question,
                /*
                This helps to check, if the quesiont /
                discussion is posted today
                It will show only the time in 12 hour format
                If not, it will show the date and time in 12 hour format
                This helps for users to find new discussions easily
                */
                CASE
                    WHEN DATE(Q.created_at) = DATE('now', 'localtime')
                    THEN STRFTIME('%I:%M %p', TIME(Q.created_at))
                    ELSE STRFTIME('%Y-%m-%d %I:%M %p', Q.created_at)
                END AS created_at,
                CASE
                    WHEN U.user_id = :uid THEN 'You'
                    ELSE U.full_name
                END AS posted_user,
                CASE
                    WHEN U.profile_image NOT LIKE 'https%'
                    THEN :static_base || U.profile_image
                    ELSE U.profile_image
                END AS profile_image_url,
                COUNT(A.answer_id) AS number_of_answers,
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM Saved_question SQ
                        WHERE SQ.question_id = Q.question_id
                            AND SQ.user_id = :uid
                    )THEN 'saved'
                    ELSE 'unsaved'
                END AS save_status
            FROM
                Question Q
            JOIN
                User U ON U.user_id = Q.user_id
            LEFT JOIN
                Answer A ON A.question_id = Q.question_id
        """
    grouping_and_ordering_query = """
            GROUP BY
                Q.question_id
            ORDER BY Q.created_at DESC
        """

    since_query = "WHERE Q.created_at > :since_ts"

    # When I add the filter_query,
    # I have added WHERE part,
    # Therefore I added AND instead of WHERE
    if filter_query != "":
        # keeps a space before "AND" otherwise,
        # when we combine them without a space
        # there would be an error in SQL
        since_query = " AND Q.created_at > :since_ts"

    full_query = base_query + filter_query + \
        since_query + grouping_and_ordering_query

    question_cards_detail_from_db = db_execute(query=full_query,
                                               fetch=True,
                                               values={
                                                   "uid": user_id,
                                                   "static_base": static_base,
                                                   "since_ts": since_ts[0]})
    if question_cards_detail_from_db:
        question_cards_detail = []
        # Removes all the markdown format for better user readability
        for question_card in question_cards_detail_from_db:
            temp_list = list(question_card)
            temp_list[1] = strip_markdown.strip_markdown(question_card[1])
            question_cards_detail.append(temp_list)
        return question_cards_detail
    else:
        return "", 200


# An intermediate function between the relevant routes
#   and get_community_questions_from_db()
# to reduce the code repetition
def get_community_questions_from_db_with_since(query: str):
    """
    This function calls the get_community_questions_from_db(),
        with the since_id from the frontend

    Args:
        - query (string): stores the query that is used to filter,
          in different routes.

    Flow:
    Route Function
        │   ▲
        │   │return
        ▼   │
    get_community_questions_from_db_with_since
        │   ▲
        │   │return
        ▼   │
    get_community_questions_from_db

    Return:
        - An array: Includes question_id, question with no markdown codes,
                    created time, person who asked the question,
                    profile image URL, number of answers, and save status
        - or a string: "" (if there are no questions)
    """
    data = request.get_json()
    since_id = data.get("since_id")
    question_cards_detail = get_community_questions_from_db(query, since_id)
    return question_cards_detail


# Route that displays all community questions that happened in the platform
@community_bp.route("/community")
@login_required
def all_community_questions():
    """
    Render the community questions page.
    """
    return render_template(
        "user/community/community-all.html",
    )


# This Route connects with the client side, and each 2500 milliseconds
# it calls the get_all_community_questions function to keep the data updated
@community_bp.route("/community/get-all-questions", methods=["POST"])
@login_required
def get_all_community_questions():
    """
    Retrieve all community questions.

    Returns:
        Response: A JSON response containing the list of all community
        questions retrieved from the database.
    """
    return jsonify(get_community_questions_from_db_with_since(""))


# Route that displays all community questions that happened on one day
@community_bp.route("/community/newest")
@login_required
def newest_community_questions():
    """
    Render the new community questions page.
    """
    return render_template("user/community/community-new.html")


# This routes also connects with the client side, and in each 2.5 seconds
# It sends the questions that have been posted today
# This helps for the users to find new discussions easily
@community_bp.route("/community/get-new-questions", methods=["POST"])
@login_required
def get_new_community_questions():
    """
    Retrieve new community questions.

    Returns:
        Response: A JSON response containing the list of new community
        questions retrieved from the database.
    """

    query = "WHERE  DATE(Q.created_at) = DATE('now', 'localtime')"
    return jsonify(
        get_community_questions_from_db_with_since(query))


# Routes that displays all questions that have done by the user
@community_bp.route("/community/you")
@login_required
def user_community_questions():
    """
    Render the community questions page that are done by the user.
    """
    return render_template("user/community/community-user.html")


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have been posted by the relevant logged in user
# This helps user to find answers for their questions easily
@community_bp.route("/community/get-user-posted-questions", methods=["POST"])
@login_required
def get_user_posted_questions():
    """
    Retrieve users' community questions.

    Returns:
        Response: A JSON response containing the list of users' community
        questions retrieved from the database.
    """
    query = "WHERE Q.user_id = :uid"
    return jsonify(
        get_community_questions_from_db_with_since(query))


# Route that displays all community questions that have not been answered
@community_bp.route("/community/unanswered")
@login_required
def unanswered_community_questions():
    """
    Render the unanswered community questions page.
    """
    return render_template("user/community/community-unanswered.html")


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have not been answered yet
@community_bp.route("/community/get-unanswered-questions", methods=["POST"])
@login_required
def get_unanswered_questions():
    """
    Retrieve all unanswered community questions.

    Returns:
        Response: A JSON response containing the list of
        all unanswered community
        questions retrieved from the database.
    """
    query = "WHERE A.answer_id IS NULL"
    return jsonify(
        get_community_questions_from_db_with_since(query))


# Route that displays all community questions that have been saved by the user
@community_bp.route("/community/saved")
@login_required
def saved_community_questions():
    """
    Render the saved community questions page.
    """
    return render_template("user/community/community-saved.html")


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have been saved by the user
# This helps to user group questions that they think are important
@community_bp.route("/community/get-saved-questions", methods=["POST"])
@login_required
def get_saved_questions():
    """
    Retrieve saved community questions.

    Returns:
        Response: A JSON response containing the list of saved community
        questions retrieved from the database.
    """
    query = """
            WHERE EXISTS (
            SELECT 1
            FROM Saved_question SQ
            WHERE SQ.question_id = Q.question_id
                AND SQ.user_id = :uid )
    """
    return jsonify(get_community_questions_from_db_with_since(query))


# Route the adds a new post to the community
@community_bp.route("/community/add-new-post", methods=["POST"])
@login_required
def add_new_post():
    """
    Adds new questions that are created by users.
    Before adding to the database, it checks whether the question is not empty,
    and within the limit
    (minimum is 30 characters and maximum is 30000 characters).
    It creates a unique question ID and saves it to the database,
    with the question ID, user ID, question, and created date.
    The function uses the datetime library to generate
    the current date and time. This route has connected "postTheQuestion""
    function in the community-base.js file.

    Returns:
        - If the question is empty,
          it sends a “You need to enter something before posting your question”
          warning message to the frontend.
        - If the question is more than 30000 characters,
          it sends a “Limit exceeded: 30,000 characters” warning message
        - If the question is less than 30 characters,
          it sends a “Question is too short.
          Please provide more details (at least 30 characters)” warning message
        - If the question is successfully created, it saves to the database,
          and sends “🎉 Success! Your question is now live.” success message,
          with 200 HTTP code
    """
    data = request.json

    user_input = data.get("userQuestionInput")

    # Check the validity of the user input,
    # if it is not empty save to the database
    # If it is empty, do not save to the database
    if not user_input.strip():
        return jsonify({"message_type": "warning",
                        "message": ("You need to enter something"
                                    " before posting your question")})

    characters_limit_result = check_characters_limit(user_input,
                                                     max_length=30000,
                                                     min_length=30)
    if characters_limit_result == 'max_reject':
        return jsonify({"message_type": "warning",
                        "message": "Limit exceeded: 30,000 characters."})

    elif characters_limit_result == "min_reject":
        return jsonify({"message_type": "warning",
                        "message": (
                            "Question is too short."
                            " Please provide more details"
                            " (at least 30 characters).")})

    question_id = str(uuid.uuid4())
    user_id = session.get("user_id")
    question = user_input
    created_at = datetime.now().isoformat(timespec="seconds")

    insert_query = """
            INSERT
            INTO Question (question_id,
                            user_id,
                            question,
                            created_at)
            VALUES (?, ?, ?, ?)"""

    db_execute(query=insert_query,
               values=(question_id,
                       user_id,
                       question,
                       created_at,
                       ))
    return jsonify({"message_type": "success",
                    "message": "🎉 Success! Your question is now live."}), 200


# Route the handles the save and unsave functionality of a discussion
@community_bp.route("/community/toggle-save", methods=["POST"])
@login_required
def toggle_save():
    """
    Controls the saving questions.
    If the user has saved a question,
    and if the user clicks on the save toggle icon again,
    it unsaves that question, and vice versa.

    It gets the question ID from the frontend and checks
    with the backend before the saving and unsaving process.
    If the validation is successful, it checks, there is any ID
    (saved_question_id) in the Saved_question table in the Database
    (uses user_id from the session variable).
    If there is an ID, it deletes that row from the table;
    If there is no ID, it inserts a new row.
    It has connected to the toggleSave() function in the
    community-utils.js

    Returns:
        - Response: A flask JSON response containing the save status
          (yes or no), with 200 HTTP code
    """
    data = request.get_json()
    client_question_id = data["questionId"]

    # Valide the question_id coming from the client side with the
    # database
    question_id_query = """
                    SELECT
                        question_id
                    FROM question
                    WHERE question_id = ?"""

    question_id = db_execute(query=question_id_query,
                             fetch=True,
                             fetchone=True,
                             values=(client_question_id,))
    is_save = "no"

    if question_id:
        user_id = session.get("user_id")

        # Ckeck has user saved that discussion
        # NOTE: Couldn't combine this with SQl query,
        # Because I have to pass that 'is_save' to frontend
        save_question_id_query = """
                SELECT
                    saved_question_id
                FROM Saved_question
                WHERE question_id=? AND user_id=?"""

        saved_question_id_from_db = db_execute(query=save_question_id_query,
                                               fetch=True,
                                               fetchone=True,
                                               values=(question_id[0],
                                                       user_id,
                                                       ))

        # if user has saved, delete the saved discussion
        # from the saved_question table
        # if user has not saved, insert a new row to the saved_question table
        # and set the isSave variable to "yes" or "no" accordingly,
        # this helps for the frontend to show the correct icon
        if saved_question_id_from_db:
            delete_query = """
                DELETE FROM Saved_question
                WHERE saved_question_id=?"""

            db_execute(query=delete_query,
                       values=saved_question_id_from_db)

            is_save = "no"
        else:
            insert_query = """
                INSERT INTO
                    Saved_question
                    (saved_question_id, question_id, user_id)
                VALUES (?, ?, ?)
            """
            saved_question_id = str(uuid.uuid4())
            db_execute(query=insert_query,
                       values=(saved_question_id, question_id[0], user_id))
            is_save = "yes"

    return jsonify({"isSave": is_save}), 200


# This route shows the all the answers relevant to clicked question
@community_bp.route("/community/<question_id>/discussions")
@login_required
def discussions(question_id: str):
    """
    Gets the question, and
        if there is markdown code in that question,
        it converts it to the html code.
    It compares the question_id in the session with the question_id
        from the frontend. If they are not equal, it redirects to
        the 'community.all_community_questions'.
        Otherwise, it gets the question ID, question, created date,
        posted user, profile image URL, and save status from the database.

    Args:
        - question_id (string): Used to check the question ID
                                that comes from the frontend

    Returns:
        - If the program gets all the data successfully,
          it renders the discussion.html; otherwise,
          it redirects to the “community.all_community_question”.
    """
    if question_id != session.get("question_id"):
        return redirect(url_for("community.all_community_questions"))

    user_id = session.get("user_id")
    static_base = url_for('static', filename='')
    query = """
                SELECT
                    Q.question_id,
                    Q.question,
                    /*
                    This helps to check, if the quesiont /
                    discussion is posted today
                    It will show only the time in 12 hour format
                    If not, it will show the date and time in 12 hour format
                    This helps for users to find new discussions easily
                    */
                    CASE
                        WHEN DATE(Q.created_at) = DATE('now', 'localtime')
                        THEN STRFTIME('%I:%M %p', TIME(Q.created_at))
                        ELSE STRFTIME('%Y-%m-%d %I:%M %p', Q.created_at)
                    END AS created_at,
                    CASE
                        WHEN U.user_id = :uid THEN 'You'
                        ELSE U.full_name
                    END AS posted_user,
                    CASE
                        WHEN U.profile_image NOT LIKE 'https%'
                        THEN :static_base || U.profile_image
                        ELSE U.profile_image
                    END AS profile_image_url,
                    COUNT(A.answer_id) AS number_of_answers,
                    CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM Saved_question SQ
                            WHERE SQ.question_id = Q.question_id
                                AND SQ.user_id = :uid
                        )THEN 'saved'
                        ELSE 'unsaved'
                    END AS save_status
                FROM
                    Question Q
                JOIN
                    User U ON U.user_id = Q.user_id
                LEFT JOIN
                    Answer A ON A.question_id = Q.question_id
                WHERE Q.question_id = :qid
                """
    question_details_from_db = db_execute(query=query,
                                          fetch=True,
                                          values={"uid": user_id,
                                                  "qid": question_id,
                                                  "static_base": static_base})

    if not question_details_from_db:
        return redirect(url_for("community.all_community_questions"))

    # Checks the question id is not empty
    # This is because if a user delete his account,
    # the question id will be empty
    # then at the same time, if another user reads the discussion,
    # there will be an error
    # To avoid that error, we check if the question id is not empty
    # question_details_from_db[0][0] is the question id
    if question_details_from_db[0][0]:
        question_details_that_goes_to_client_side = list(
            question_details_from_db[0])
        if question_details_that_goes_to_client_side[1]:
            question_details_that_goes_to_client_side[1] = markdown.markdown(
                question_details_that_goes_to_client_side[1],
                extensions=['fenced_code'])
        return render_template(
            "user/community/discussions.html",
            question_detail=question_details_that_goes_to_client_side,
        )
    else:
        return redirect(
            url_for("community.all_community_questions"))


# This Route validates the question_id coming from
# the client side with the database question_id
# It passes the redirect url to the client side to change the page
@community_bp.route("/community/check-qid", methods=["POST"])
@login_required
def check_qid():
    """
    This route is used to validate the question ID
        that comes from the frontend, and if the validation is successful,
        it saves that ID into session variables (session[“question_id”]).

    This function has connected with the openTheDiscussion() function
        in the question-card.js file. This function is called before
        the user goes to the discussion page.


    Returns:
        - Response: If both IDs (client side and backend) are equal,
          it sends a JSON response containing the redirect URL
          for the discussion page
        - If the IDs do not match, it redirects to the
          "community.all_community_questions"
    """
    data = request.get_json()
    client_question_id = data["questionId"]

    # Uses the client side question id to check
    # if there is an actual question id in the database
    # If there is a question id in the database, it will set the
    # session question_id
    query = "SELECT question_id FROM question WHERE question_id = ?"

    question_id = db_execute(query=query,
                             fetch=True,
                             fetchone=True,
                             values=(client_question_id,))

    if question_id:
        session["question_id"] = client_question_id
        redirect_url = url_for(
            "community.discussions", question_id=client_question_id
        )
        return jsonify({"redirect_url": redirect_url})
    else:
        return redirect(
            url_for("community.all_community_questions"))


# Route that adds answers to the relevant question
@community_bp.route("/community/add-answers", methods=["POST"])
@login_required
def add_answers():
    """
    This route is used to add answers for relevant questions
        that are asked by other users.
    First, it checks whether, input is empty or within the relevant
        character limits. If all is fine, it inserts that into the database.
        This route has connected with the addAnswers() function
        in the discussions.js

    Returns:
        - Response: If the process is successful, it sends a JSON response
          containing a successful message, called "🎉 Added!”"
        - Response: If there is an issue with the number of characters,
          it sends the suitable warning message,
          either "Answer is too long.. Maximum allowed is 20,000 characters,"
          or "Answer is too short.
          Please provide more details (minimum 30 characters)."
        - Response: If the input is empty,
          it sends "Answer cannot be empty. Please type your answer."
    """
    data = request.get_json()
    user_answer = data["userAnswer"]

    # Before adding to the database, check userinput is not a blank or
    # empty string
    if not user_answer.strip():
        return jsonify({"message_type": "warning",
                        "message": ("Answer cannot be empty. "
                                    "Please type your answer")})

    # Validate the number of characters
    characters_limit_result = check_characters_limit(user_answer,
                                                     max_length=20000,
                                                     min_length=30)
    if characters_limit_result == "min_reject":
        return jsonify({"message_type": "warning",
                        "message": ("Answer is too short. "
                                    "Please provide more details "
                                    "(minimum 30 characters).")})

    if characters_limit_result == "max_reject":
        return jsonify({"message_type": "warning",
                        "message": ("Answer is too long. "
                                    "Maximum allowed is 20,000 characters.")})

    created_at = datetime.now().isoformat(timespec="seconds")
    answer_id = str(uuid.uuid4())
    question_id = session.get("question_id")
    user_id = session.get("user_id")
    insert_query = """
                    INSERT
                    INTO Answer
                        (answer_id,
                        question_id,
                        user_id,
                        content,
                        created_at)
                    VALUES (?, ?, ?, ?, ?)"""

    db_execute(query=insert_query,
               values=(answer_id,
                       question_id,
                       user_id,
                       user_answer,
                       created_at))

    return jsonify({"message_type": "success", "message": "🎉 Added!"}), 200


# This route gets all the answers that are relevant
# to the question that user clicked
# THis route passes the answers to the client side in every 2.5 seconds
# To keep anwers updated
@community_bp.route("/community/get-answers", methods=['POST'])
@login_required
def get_answers():
    """
    This route sends all the answers related to a specific question.
    It takes the user_id from the session variables,
            and creates a static base
            (This is for the images that are not starting from "https").
            This function gets the last ID through the parameter
            called 'since_id'.
            This is due to the current system using the polling method
            to keep updating the page; therefore,
            the program wants the last ID (since_id) to get the last time
            that fetch happened. It can be empty.
        Answers that are done by the login user will change to
            “You” instead of the full own name
        Answers that happen during the current date show only the time
    This route has been connected with the getAnswers() function
    in the discussions.js

    Returns:
        - An array: Includes answer_id, answer,
                    created time, person who gave the answer,
                    profile image url, number of likes, and like status
    """
    data = request.get_json()
    since_id = data.get("since_id")

    question_id = session.get("question_id")
    static_base = url_for('static', filename='')
    user_id = session.get("user_id")

    since_ts_query = """
                SELECT
                    created_at
                FROM Answer
                WHERE answer_id = ?
                """

    since_ts = db_execute(query=since_ts_query,
                          fetch=True,
                          fetchone=True,
                          values=(since_id, ))

    # ts: time stamp
    if since_ts:
        since_ts = since_ts[0]
    else:
        since_ts = ""

    query = """
        SELECT
            A.answer_id,
            A.content,
            CASE
            WHEN DATE(A.created_at) = DATE('now', 'localtime')
                THEN
                STRFTIME('%I:%M %p', TIME(REPLACE(A.created_at, 'T', ' ')))
                ELSE
                STRFTIME('%Y-%m-%d %I:%M %p', REPLACE(A.created_at, 'T', ' '))
            END AS created_at,
            CASE
            WHEN U.user_id = :uid THEN 'You'
                ELSE U.full_name
            END AS answered_user,
            CASE
            WHEN U.profile_image NOT LIKE 'https%'
                THEN :static_base || U.profile_image
                ELSE U.profile_image
            END AS profile_image_url,
            COUNT(AL.answer_id) AS number_of_likes,
            CASE
            WHEN EXISTS (
                SELECT 1
                    FROM AnswerLike AL
                    WHERE A.answer_id = AL.answer_id
                        AND A.user_id = :uid
                )THEN 'like'
                ELSE 'unlike'
            END AS like_status
        FROM Answer A
        JOIN User U ON U.user_id = A.user_id
        LEFT JOIN AnswerLike AL ON AL.answer_id = A.answer_id
        WHERE question_id = :qid
            AND A.created_at > :since_ts
        GROUP BY A.answer_id
        ORDER BY A.created_at ASC
        """

    answers_details_that_go_to_the_frontend = db_execute(
        query=query,
        fetch=True,
        values={
            "uid": user_id,
            "qid": question_id,
            "static_base": static_base,
            "since_ts": since_ts})

    return jsonify(answers_details_that_go_to_the_frontend)


# This route handles the like and unlike functionality of the answers
# If user has likes the answer it will comver to unlike and other way around
# It also counts the number of likes for the answer and sends it to the
# client side
@community_bp.route("/community/toggle-like", methods=["POST"])
@login_required
def toggle_like():
    """
    This route controls the like toggle for answers.
    It gets the answer ID from the client side,
        uses that value to check if there is any row in the AnswerLike table.
        If there is any row, it deletes that row from the table; otherwise,
        it inserts a new row. This route has connected with the toggleLike()
        function in the discussions.js

    Returns:
        - Response: A JSON with a like status and the number of likes
    """
    data = request.get_json()

    # No validation required, as the system doesn't crash
    # if the user changes the answerId
    client_answer_id = data["answerId"]
    user_id = session.get("user_id")

    liked_answer_id_query = """
                            SELECT like_id
                            FROM AnswerLike
                            WHERE user_id=? AND answer_id=?"""

    liked_answer_id_from_db = db_execute(query=liked_answer_id_query,
                                         fetch=True,
                                         fetchone=True,
                                         values=(user_id,
                                                 client_answer_id,
                                                 ))

    # if the liked_answer_id has some kind of value
    # it will delete from the AnswerLike table,
    # and set the like variable to "no"
    # IF there is no value in the liked_answer_id_from_db,
    # It will insert the new like answers details to the AnswerLike table
    # and set the like variable to "yes"
    if liked_answer_id_from_db:
        delete_query = "DELETE FROM AnswerLike WHERE like_id=?"
        db_execute(query=delete_query,
                   values=(liked_answer_id_from_db[0], ))
        like = "no"
    else:
        like_id = str(uuid.uuid4())
        insert_query = """
            INSERT INTO
            AnswerLike (like_id, user_id, answer_id) VALUES (?, ?, ?)"""
        db_execute(query=insert_query,
                   values=(like_id,
                           user_id,
                           client_answer_id))
        like = "yes"

    # Counts the number of likes for the answer
    # and sends it to the client side
    number_of_likes_query = """
                        SELECT COUNT(*) FROM AnswerLike WHERE answer_id=?
                        """
    number_of_likes = db_execute(query=number_of_likes_query,
                                 fetch=True,
                                 fetchone=True,
                                 values=(client_answer_id,))

    return jsonify({"like": like, "nu_likes": number_of_likes[0]})


# This route gets the number of answers for the relevant question
# This has connected with the client side, and pass data in every 2.5 seconds
# to keep the number of answers updated
@community_bp.route("/community/get-number-of-answers")
@login_required
def get_number_of_answers():
    """
    This route sends the number of answers
        every 2.5 seconds when the frontend calls.
    This route has connected with the updateNumberofAnswers()
        function in the discussions.js

    Returns:
        - Response: A JSON with the number of likes
    """
    question_id = session.get("question_id")

    query = "SELECT COUNT(*) FROM Answer WHERE question_id = ?"
    number_of_answers = db_execute(query=query,
                                   fetch=True,
                                   fetchone=True,
                                   values=(question_id,))

    return jsonify({"numberOfAnswers": number_of_answers})


# Removes the punctuations of a text
# This is used in below
translator = str.maketrans('', '', string.punctuation)


# This route filters the questions based on the user's keywords
# This route will only work if the keyword is not empty or just whitespace
@community_bp.route("/community/search/", methods=["GET"])
@login_required
def search_questions():
    """
    This route uses a simple algorithm for searching questions.
    (The reason not to use the SQL query is that the user
        does not type the exact keywords.)

    Process of Algorithm:
        1. Convert all the questions into plain text without emojis,
            punctuation
        2. Then, convert that to a set (to remove all the duplicates)
        3. Then compare the keywords' length and the question's length
        4. Save the smaller value in the denominator
        5. Removes all the duplicates of both keywords and the question
        6. And count the similar words in both sets
        7. And gets a percentage (similar words/denominator) * 100
        8. If the percentage is higher than 50, it appends to the
            search_result array
        9. Repeat for every Question

    Note: There are some limitations for the algorithm.
          Through testing, 90% accuracy is there

    Returns:
        - Renders the community-search-result.html with the search_result
          array,  otherwise it redirects to the
          "community.all_community_questions"
    """
    keyword = request.args.get("search")
    search_result = []
    # Uses this algorithm, because
    # because the user doens not type the exact
    #   key words
    if not keyword == "" and not keyword.isspace():
        question_cards_detail = get_community_questions_from_db("", "")
        for question_card_detail in question_cards_detail:

            # Converts the question from the database to plain text
            # This makes it easier to convert into a flat array
            flat_question = question_card_detail[1].replace(
                '\r\n', ' ').replace('\n', ' ')

            # Removes existing emojis, otherwise,
            # the algorithm doesn't work properly
            # because can't find similar words between the question and
            # the keyword
            emojiless_question = emoji.replace_emoji(
                flat_question, replace="")

            # Removes exisiting punctuation marks,
            # and converts to lowercase
            clean_question = emojiless_question.translate(
                translator).lower()

            # Convert the exisitng cleaned string to an array then a set
            # Because It removes duplicate values
            # If there are duplicate values, calculation maybe wrong
            # At last converts it to an array
            question_array = list(set(clean_question.split(" ")))

            # Converts the User input to a plain text without any symbols
            # This makes it easier to convert into a flat array
            emojiless_keyword = emoji.replace_emoji(
                keyword, replace="")

            # Removes exisiting punctuation marks,
            # and converts to lowercase
            clean_keyword = emojiless_keyword.translate(
                translator).lower()

            # Convert the exisitng cleaned string to an array then a set
            # Because It removes duplicate values
            # If there are duplicate values, calculation maybe wrong
            # At last converts it to an array
            keyword_array = list(set(clean_keyword.split(" ")))

            # Compare the lenght of those created arrays,
            # And save the array that has small number of elements
            # to a varaible called denominator
            # This is done because, if we use the bigger value,
            # our percentage will be getting lower
            # To avoid that I take the smallest lenght of array and
            # count it lenght and save it.
            if len(question_array) < len(keyword_array):
                denominator = len(question_array)
            else:
                denominator = len(keyword_array)

            # Converts created two arrays into two tuple
            # Then we can find the simillar words between those two
            # arrays
            keyword_set = set(keyword_array)
            question_set = set(question_array)

            # Counts the similar words between two tuples
            nu_common_words = len(
                question_set.intersection(keyword_set))

            # Finds the percentage of quility between two arrays
            percentage_of_equility = (
                nu_common_words / denominator) * 100

            # If the percentage is increased than 50
            # append to the search_result array
            # I chose 50 because it is a fair value and the center of
            # 100
            if percentage_of_equility >= 50:
                search_result.append(question_card_detail)

        return render_template(
            "user/community/community-search-result.html",
            search_result=search_result)
    else:
        return redirect(url_for("community.all_community_questions"))
