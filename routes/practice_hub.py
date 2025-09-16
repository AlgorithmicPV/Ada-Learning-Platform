import uuid
from flask import (Blueprint,
                   render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   jsonify)
import markdown
from utils import db_execute, login_required

practice_hub_bp = Blueprint("practice_hub", __name__)


# This function works only for the searching
# and uncomplete challenges
def get_practice_challenges(search_key: str = None):
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
    return challenges

# This Route shows the all the unsolved Challenges


@practice_hub_bp.route("/practice-hub")
@login_required
def uncomplete_practice_challenges():
    unsolved_challenges = get_practice_challenges()

    # I assigned the page title in here
    # Because I am using the same template to show the search result
    page_title = "Unsolved"
    return render_template(
        "user/practice_hub/unsolved-challenges.html",
        page_title=page_title,
        challenges=unsolved_challenges)


# This route validates the challenge ids comming
# from the client side with the database and save it to the session data
# This route will work when the user cicks on a challenge
# if that clicked challenge's status is not started or completed,
# It will mark it as "Started"
# If the challenge id is validate,
# this will redirect to the route that shows the challenge and
# code editor to do the challenge
@practice_hub_bp.route("/practice-hub/validate-challenge-id", methods=["POST"])
@login_required
def validate_challenge_id():
    client_challenge_id = request.form.get("challenge_id")

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
                                      values=(client_challenge_id,))

    if challenge_id_from_db:
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
                           'cid': client_challenge_id})

        session["challenge_id"] = client_challenge_id

        challenge_title_query = """
                        SELECT challenge_title
                        FROM Challenge
                        WHERE challenge_id=?
                        """

        challenge_title = db_execute(query=challenge_title_query,
                                     fetch=True,
                                     fetchone=True,
                                     values=(client_challenge_id,))[0]

        # Formates the challenge title,
        # if there are space converted them into "-"
        # For better user experence
        formated_challenge_title = challenge_title.replace(" ", "-")

        return redirect(
            url_for(
                "practice_hub.show_challenge",
                challenge_title=formated_challenge_title))
    else:
        return redirect(
            url_for("practice_hub.uncomplete_practice_challenges"))


# This Route shows the Challenge and the code editor etc..
@practice_hub_bp.route("/practice-hub/<challenge_title>")
@login_required
def show_challenge(challenge_title):
    session["language"] = "python"

    challenge_id = session.get("challenge_id")
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
