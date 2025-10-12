"""
Handles all the routes and fucntions related to Practice Hub section
"""

import uuid
from flask import (Blueprint,
                   render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   jsonify,
                   abort)
import markdown
from utils import db_execute, login_required

practice_hub_bp = Blueprint("practice_hub", __name__)


# This function works only for the searching
# and uncomplete challenges
def get_practice_challenges(search_key: str = None):
    """
    This function gets practice challenges for the logged-in user.

    If a search key is given, it finds challenges that match the
    search by title or difficulty level. If no search key is provided,
    it returns the challenges that are not yet completed by the user.
    It runs a database query to fetch the challenge id,
    number, title, difficulty level, and the user's status for each challenge,
    then sends the results back.

    Args:
        search_key (str): A word or phrase to search by challenge title or
        difficulty level. Defaults to None. * Optional

    Returns:
        - list: A list of challenges with their details and status for
              the current user.
    """
    user_id = session.get("user_id")

    common_query = """
                    SELECT
                        C.challenge_id,
                        C.number,
                        C.challenge_title,
                        C.difficulty_level,
                        CASE
                            WHEN
                                (
                                SELECT CA.status
                                FROM Challenge_attempt CA
                                WHERE CA.challenge_id = C.challenge_id
                                    AND CA.user_id = :uid
                                ) IS NULL
                            THEN '-'
                            ELSE (
                                SELECT CA.status
                                FROM Challenge_attempt CA
                                WHERE CA.challenge_id = C.challenge_id
                                    AND CA.user_id = :uid
                                )
                        END AS status
                    FROM Challenge C
                """

    unsolved_challenges_query = """
                                WHERE (
                                        SELECT CA.status
                                        FROM Challenge_attempt CA
                                        WHERE CA.challenge_id = C.challenge_id
                                            AND CA.user_id = :uid
                                    ) IS NOT 'Completed'
                                """

    search_query = """
                    WHERE challenge_title LIKE :search_kev
                    OR difficulty_level LIKE :search_kev
                    """

    if search_key:
        query = common_query + search_query
        values = {"uid": user_id, "search_kev": f"%{search_key}%"}
    else:
        query = common_query + unsolved_challenges_query
        values = {"uid": user_id}

    challenges = db_execute(query=query,
                            fetch=True,
                            values=values)
    
    # Check, if the challenges is null because of a searchkey
    # otherwise we can't get the no search result output
    if search_key:
        if not challenges:
            return "no-result"
        
    if challenges:
        return challenges
    else:
        return "completed"


# This Route shows the all the unsolved Challenges
@practice_hub_bp.route("/practice-hub")
@login_required
def uncomplete_practice_challenges():
    """
    This route shows all the unsolved challenges for the logged-in user.

    The function calls get_practice_challenges() without a search key
    to collect the challenges that are not yet completed. It then sets
    the page title as "Unsolved" and renders the template
    unsolved-challenges.html with the list of challenges
    and the page title.


    Returns:
        - Rendered HTML template with the unsolved challenges.
    """
    unsolved_challenges = get_practice_challenges()

    # I assigned the page title in here
    # Because I am using the same template to show the search result
    page_title = "Unsolved"
    return render_template(
        "user/practice_hub/unsolved-challenges.html",
        page_title=page_title,
        challenges=unsolved_challenges)


# This Route shows the Challenge and the code editor etc..
@practice_hub_bp.route("/practice-hub/<challenge_id>")
@login_required
def show_challenge(challenge_id):
    """
    Show the selected coding challenge and its code editor.

    What this does (in simple steps):
    1) Sets the default editor language to Python.
    2) Checks the challenge_id from the URL against the database.
       - If it doesn't exist, show a 404 error.
    3) If it exists, make sure the user has a Challenge_attempt row.
       If not, create one with status = "Started".
    4) Load the challenge details (title, number, question, and the
       user's current status for this challenge).
    5) Convert the question (Markdown) into HTML so it displays nicely.
    6) Render the challenge page with all that info.

    Args:
        challenge_id (str): The challenge ID from the URL.

    Returns:
        Response: The rendered challenge page with the editor,
        or a 404 error page if the ID is invalid.
    """
    session["language"] = "python"

    # Validates the challenge id comes from client side
    # with the database
    challenge_id_query = """
                    SELECT challenge_id
                    FROM Challenge
                    WHERE challenge_id=?
                    """

    challenge_id_from_db = db_execute(query=challenge_id_query,
                                      fetch=True,
                                      fetchone=True,
                                      values=(challenge_id,))

    if not challenge_id_from_db:
        abort(404)

    user_id = session.get("user_id")

    challenge_attempt_id = str(uuid.uuid4())
    insert_query = """
            -- Insert a new challenge attempt with status 'Started'
            -- if not already attempted
            INSERT INTO
                Challenge_attempt (
                                id,
                                user_id,
                                challenge_id,
                                status)
            SELECT :caid, :uid, :cid, 'Started'
            WHERE NOT EXISTS (
                SELECT 1
                FROM Challenge_attempt
                WHERE challenge_id = :cid AND user_id = :uid
            );
        """

    db_execute(query=insert_query,
               fetch=False,
               values={'caid': challenge_attempt_id,
                       'uid': user_id,
                       'cid': challenge_id})

    session["challenge_id"] = challenge_id
    query = """
                SELECT
                    challenge_id,
                    number,
                    challenge_title,
                    question,
                    (
                    SELECT status
                    FROM Challenge_attempt
                    WHERE challenge_id = :cid
                        AND user_id = :uid
                    ) as status
                FROM Challenge
                WHERE challenge_id= :cid
                """
    challenge_info = db_execute(query=query,
                                fetch=True,
                                values={"cid": challenge_id,
                                        "uid": session.get("user_id")})[0]

    challenge_info_list = list(challenge_info)
    challenge_info_list[3] = markdown.markdown(challenge_info_list[3])

    return render_template(
        "user/practice_hub/challenge.html",
        challenge_info=challenge_info_list)


# This route sends the solution for the clicked challenge
@practice_hub_bp.route("/practice-hub/solution", methods=["POST"])
@login_required
def solution_second_call():
    """
    This route sends the solution for the selected challenge
    in the chosen language.

    The function reads the request data in JSON format and
    checks the programming language, with Python set as the default.
    If the language is valid, it gets the challenge_id from
    the session and queries the Solution table for the saved answer.
    The answer is converted from markdown to HTML with code formatting
    and then returned as a JSON response. This route has connected
    to options.forEach() in challenges.js


    Returns:
        - Response: JSON object containing the solution in HTML format.
    """
    data = request.get_json()
    language = data.get("language", "python")
    languages = ["python", "c++", "java", "javascript", "typescript"]
    if language in languages:
        challenge_id = session.get("challenge_id")

        query = """
                SELECT answer
                FROM Solution
                WHERE challenge_id=? AND language=?
                """

        # Converts the markdown code to html
        answer = markdown.markdown(
            db_execute(query=query,
                       fetch=True,
                       fetchone=True,
                       values=(challenge_id, language,))[0],
            extensions=['fenced_code'])
        return jsonify({"answer": answer})


# This route sends solution to the page that shows all challenges
# When the user clicks on the solution button it will sends
# the solution for selected language through the AJAX
@practice_hub_bp.route("/practice-hub/solution-challenges", methods=["POST"])
@login_required
def solution_first_call():
    """
    This route sends the solution to the challenges page
    when the user clicks the solution button.

    The function reads the challenge_id from the request,
    validates it with the database, and if it exists, sets it in the session.
    By default, the language is set to Python. It then queries
    the Solution table to get the answer and challenge title, converts the
    answer from markdown to HTML, and
    returns both the answer and title as a JSON response.
    This route has connected to solutionShowButtons.forEach() in
    discussions.js


    Returns:
        - Response: JSON object containing the solution
                    and the challenge title.
    """
    data = request.get_json()
    client_challenge_id = data.get("value")

    challenge_id_query = """
                        SELECT challenge_id
                        FROM Challenge
                        WHERE challenge_id=?
                        """

    challenge_id_from_db = db_execute(query=challenge_id_query,
                                      fetch=True,
                                      fetchone=True,
                                      values=(client_challenge_id, ))

    if challenge_id_from_db:
        # In default language has set to python language
        language = "python"
        session["challenge_id"] = client_challenge_id
        query = """
                SELECT
                    S.answer,
                    (
                    SELECT C.challenge_title
                    FROM Challenge C
                    WHERE C.challenge_id = :cid
                    ) AS challenge_title
                FROM
                    Solution S
                WHERE
                    S.challenge_id = :cid
                    AND S.language = :lang
                """

        answer_and_title = db_execute(query=query,
                                      fetch=True,
                                      values={"cid": client_challenge_id,
                                              "lang": language})
        answer = markdown.markdown(
            answer_and_title[0][0], extensions=['fenced_code'])

        output = {
            "answer": answer,
            "title": answer_and_title[0][1]
        }

        return jsonify(output)


# This is routes shows the all the completed Challenges by the user
@practice_hub_bp.route("/practice-hub/completed")
@login_required
def completed_practice_challenges():
    """
    This route shows all the challenges completed by the logged-in user.

    The function gets the user_id from the session and queries
    the database for all challenges that the user has completed.
    It also formats the completed_at date to show only the time if finished
    today, or the full date and time otherwise.
    Finally, it renders the completed-challenges.html template with the list of
    completed challenges.


    Returns:
        - Rendered HTML template with the completed challenges.
    """
    user_id = session.get("user_id")
    completed_challenges = []

    query = """
            SELECT
                C.challenge_id,
                C.number,
                C.challenge_title,
                C.difficulty_level,
                CASE
                    WHEN DATE(CA.completed_at) = DATE('now', 'localtime')
                        THEN STRFTIME('%I:%M %p', TIME(CA.completed_at))
                        ELSE STRFTIME('%Y-%m-%d %I:%M %p', CA.completed_at)
                END AS completed_at
            FROM Challenge C
            JOIN challenge_attempt CA
                ON CA.challenge_id = C.challenge_id
                AND CA.status = 'Completed'
                AND CA.user_id = ?
        """
    completed_challenges = db_execute(query=query,
                                      fetch=True,
                                      values=(user_id,))
    return render_template(
        "user/practice_hub/completed-challenges.html",
        challenges=completed_challenges)


# Route that filters the challenges by the users' Keywprds
@practice_hub_bp.route("/practice-hub/search", methods=["GET"])
@login_required
def search():
    """
    This route filters challenges by the keyword entered by the user.

    The function gets the keyword from the request arguments and converts it to
    lowercase for case-insensitive searching. If the keyword is not empty or
    whitespace, it calls get_practice_challenges() to fetch matching challenges
    and shows them on the search-result.html page with the
    title "Search Result".
    If the keyword is invalid, it redirects the user back to the unsolved
    challenges page.


    Returns:
        - Rendered HTML template with the search results or a redirect
        to the unsolved challenges page.
    """
    keyword = request.args.get(
        "search"
        # Gets the keyword entered by the user and converts it to
        # lowercase for case-insensitive search
    ).lower()
    if not keyword == "" and not keyword.isspace():
        filtered_challenges = get_practice_challenges(keyword)
        return render_template(
            "user/practice_hub/search-result.html",
            challenges=filtered_challenges, page_title="Search Result"
        )
    else:
        return redirect(
            url_for("practice_hub.uncomplete_practice_challenges"))
