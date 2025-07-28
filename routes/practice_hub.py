from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import sqlite3
import uuid
from datetime import datetime, date
import markdown

practice_hub_bp = Blueprint("practice_hub", __name__)

# This Route shows the all the unsolved Challenges


@practice_hub_bp.route("/practice-hub")
def uncomplete_practice_challenges():
    if "user_id" in session:
        user_id = session.get("user_id")
        unsolved_challenges = []
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        cursor.execute(
            """
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
            WHERE (
                SELECT CA.status
                FROM Challenge_attempt CA
                WHERE CA.challenge_id = C.challenge_id
                    AND CA.user_id = :uid
            ) IS NOT 'Completed'
        """, {"uid": user_id})
        unsolved_challenges = cursor.fetchall()
        conn.close()

        # I assigned the page title in here
        # Because I am using the same template to show the search result
        page_title = "Unsolved"
        return render_template(
            "user/practice_hub/unsolved-challenges.html",
            page_title=page_title,
            challenges=unsolved_challenges)
    else:
        return redirect(url_for("auth.login"))


# This route validates the challenge ids comming
# from the client side with the database and save it to the session data
# This route will work when the user cicks on a challenge
# if that clicked challenge's status is not started or completed,
# It will mark it as "Started"
# If the challenge id is validate, this will redirect to the route that shows the challenge and
# code editor to do the challenge
@practice_hub_bp.route("/practice-hub/validate-challenge-id", methods=["POST"])
def validate_challenge_id():
    if "user_id" in session:
        if request.method == "POST":
            client_challenge_id = request.form.get("challenge_id")

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Validates the challenge id comes from client side w=
            # with the database
            cursor.execute("""
                            SELECT challenge_id
                            FROM Challenge
                            WHERE challenge_id=?
                           """, (client_challenge_id,))

            challenge_id_from_db = cursor.fetchone()

            if challenge_id_from_db:
                user_id = session.get("user_id")
                challenge_attempt_id = str(uuid.uuid4())
                cursor.execute(
                    """
                        -- Insert a new challenge attempt with status 'Started' if not already attempted
                        INSERT INTO Challenge_attempt (id, user_id, challenge_id, status)
                        SELECT :caid, :uid, :cid, 'Started'
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM Challenge_attempt
                            WHERE challenge_id = :cid AND user_id = :uid
                        );
                    """, {'caid': challenge_attempt_id, 'uid': user_id, 'cid': client_challenge_id})
                conn.commit()

                session["challenge_id"] = client_challenge_id

                cursor.execute("""
                                SELECT challenge_title
                                FROM Challenge
                                WHERE challenge_id=?
                               """, (client_challenge_id,))

                challenge_title = cursor.fetchone()[0]

                conn.close()

                # Formates the challenge title, if there are space converted them into "-"
                # For better user experence
                formated_challenge_title = challenge_title.replace(" ", "-")

                return redirect(
                    url_for(
                        "practice_hub.show_challenge",
                        challenge_title=formated_challenge_title))
            else:
                return redirect(
                    url_for("practice_hub.uncomplete_practice_challenges"))

        else:
            return redirect(
                url_for("practice_hub.uncomplete_practice_challenges"))
    else:
        return redirect(url_for("auth.login"))

# This Route shows the Challenge and the code editor etc..


@practice_hub_bp.route("/practice-hub/<challenge_title>")
def show_challenge(challenge_title):
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        session["language"] = "python"

        challenge_id = session.get("challenge_id")
        cursor.execute("""
            SELECT challenge_id,
                    number,
                    challenge_title,
                    question FROM Challenge WHERE challenge_id=?
                    """, (challenge_id,))
        challenge_info = cursor.fetchall()[0]
        challenge_info_list = list(challenge_info)
        challenge_info_list[3] = markdown.markdown(challenge_info_list[3])

        conn.close()

        return render_template(
            "user/practice_hub/challenge.html",
            challenge_info=challenge_info_list)
    else:
        return redirect(url_for("auth.login"))


# This route sends the solution for the clicked challenge
@practice_hub_bp.route("/practice-hub/solution", methods=["POST"])
def solution():
    if "user_id" in session:
        if request.method == "POST":
            data = request.get_json()
            language = data.get("language")
            print(language)
            languages = ["python", "c++", "java", "javascript", "typescript"]
            if language in languages:
                challenge_id = session.get("challenge_id")

                conn = sqlite3.connect("database/app.db")
                cursor = conn.cursor()

                cursor.execute("""
                            SELECT answer
                            FROM Solution
                            WHERE challenge_id=? AND language=?
                            """, (challenge_id, language,))
                # Converts the markdown code to html
                answer = markdown.markdown(
                    cursor.fetchone()[0], extensions=['fenced_code'])
                print(answer)
                return jsonify({"answer": answer})
    else:
        return redirect(url_for("auth.login"))

# This route sends solution to the page that shows all challenges
# When the user clicks on the solution button it will sends
# the solution for selected language through the AJAX
# In default it has set to python language


@practice_hub_bp.route("/practice-hub/solution-challenges", methods=["POST"])
def solutions():
    if "user_id" in session:
        if request.method == "POST":
            data = request.get_json()
            client_challenge_id = data.get("value")

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            cursor.execute("""
                            SELECT challenge_id
                            FROM Challenge
                            WHERE challenge_id=?
                           """, (client_challenge_id,))

            challenge_id_from_db = cursor.fetchone()

            if challenge_id_from_db:
                language = "python"
                cursor.execute("""
                            SELECT answer
                            FROM Solution
                            WHERE challenge_id=? AND language=?
                            """, (client_challenge_id, language,))
                session["challenge_id"] = client_challenge_id
                answer = markdown.markdown(
                    cursor.fetchone()[0], extensions=['fenced_code'])

                cursor.execute("""
                    SELECT
                    challenge_title
                    FROM Challenge WHERE challenge_id=?
                    """, (client_challenge_id,))

                title = cursor.fetchone()[0]

                output = {
                    "answer": answer,
                    "title": title
                }
                conn.close()
                return jsonify(output)
    else:
        return redirect(url_for("auth.login"))

# This is routes shows the all the completed Challenges by the user


@practice_hub_bp.route("/practice-hub/completed")
def completed_practice_challenges():
    if "user_id" in session:
        user_id = session.get("user_id")
        completed_challenges = []
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        cursor.execute(
            """
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
            """, (user_id,))
        completed_challenges = cursor.fetchall()
        conn.close()

        return render_template(
            "user/practice_hub/completed-challenges.html",
            challenges=completed_challenges)
    else:
        return redirect(url_for("auth.login"))

# Route that filters the challenges by the users' Keywprds


@practice_hub_bp.route("/practice-hub/search", methods=["GET"])
def search():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        if request.method == "GET":
            keyword = request.args.get(
                "search"
                # Gets the keyword entered by the user and converts it to
                # lowercase for case-insensitive search
            ).lower()
            if not keyword == "" and not keyword.isspace():
                cursor.execute("""
                       SELECT challenge_id,
                                number,
                                challenge_title,
                                difficulty_level
                                FROM Challenge
                        WHERE challenge_title LIKE ?
                            OR difficulty_level LIKE ?
                       """, ((f'%{keyword}%', f'%{keyword}%')))
                filtered_challenges = cursor.fetchall()
                return render_template(
                    "user/practice_hub/search-result.html",
                    challenges=filtered_challenges, page_title="Search Result"
                )
            else:
                return redirect(
                    url_for("practice_hub.uncomplete_practice_challenges"))
    else:
        return redirect(url_for("auth.login"))
