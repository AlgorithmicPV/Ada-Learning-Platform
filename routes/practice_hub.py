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

        cursor.execute("""SELECT challenge_id,
                                number,
                                challenge_title,
                                difficulty_level
                                FROM Challenge""")
        all_challenges = cursor.fetchall()

        # Finds the status of each challenge,
        # If the status is None, appends "-" to the unsolve_challenges
        # That sign helps user to indetify that user hasn't done that challenge
        # If the status's value is "Started" it will append that value
        # This means user has started the challenge but hasn't done
        # I used status[0] because when we get data from the database we get it
        # as a tuple
        for challenge in all_challenges:
            cursor.execute("""
                          SELECT status
                           FROM Challenge_attempt
                           WHERE challenge_id=? AND
                           user_id=?""", (challenge[0], user_id,))

            status = cursor.fetchone()
            if status is None:
                challenge += ("-",)
                unsolved_challenges.append(challenge)

            if status:
                if status[0] == "Started":
                    challenge += ("Started",)
                    unsolved_challenges.append(challenge)

        # I assigned the page title in here
        # Because I am using the same template to show the search result
        page_title = "Unsolved"
        conn.close()
        return render_template(
            "user/practice_hub/unsolved_challenges.html",
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

            cursor.execute("""
                            SELECT challenge_id
                            FROM Challenge
                            WHERE challenge_id=?
                           """, (client_challenge_id,))

            challenge_id_from_db = cursor.fetchone()

            if challenge_id_from_db:
                user_id = session.get("user_id")
                cursor.execute("""
                              SELECT status
                               FROM Challenge_attempt
                               WHERE challenge_id=? AND
                               user_id=?""", (client_challenge_id, user_id,))

                status = cursor.fetchone()
                if status is None:
                    challenge_attempt_id = str(uuid.uuid4())
                    cursor.execute("""
                                INSERT INTO
                                Challenge_attempt
                                (id, user_id, challenge_id, status) VALUES
                                (?, ?, ?, ?)
                               """, (challenge_attempt_id, user_id, client_challenge_id, "Started"))
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

        # Gets all the Challenges from the database
        cursor.execute("""SELECT challenge_id,
                                number,
                                challenge_title,
                                difficulty_level
                                FROM Challenge""")
        all_challenges = cursor.fetchall()

        # Selects all the Challenges that the user has completed
        # Then those Challeneges are added to the completed_challenges list
        for challenge in all_challenges:
            cursor.execute("""
                          SELECT status
                           FROM Challenge_attempt
                           WHERE challenge_id=? AND
                           user_id=?""", (challenge[0], user_id,))

            status = cursor.fetchone()
            if status:
                if status[0] == "Completed":

                    # Gets dates that relevant challenge are completed
                    # IF the date is today it will show the time 
                    # This if for better user expereince
                    cursor.execute("""
                                SELECT completed_at FROM
                                Challenge_attempt
                                WHERE challenge_id=? AND
                                user_id=?""", (challenge[0], user_id,))
                    completed_at_from_db = cursor.fetchone()[0]
                    format_string = "%Y-%m-%dT%H:%M:%S"
                    today = date.today()

                    completed_date = completed_at_from_db.split("T")[0]

                    if str(today) == completed_date:
                        time_str = completed_at_from_db.split("T")[1]
                        time_obj = datetime.strptime(time_str, "%H:%M:%S")
                        time_12hr = time_obj.strftime("%I:%M %p")
                        challenge += (time_12hr,)
                    else:
                        format_string = "%Y-%m-%dT%H:%M:%S"
                        challenge += (
                            str(
                                (
                                    datetime.strptime(
                                        completed_at_from_db, format_string
                                    )
                                ).strftime("%Y-%m-%d %I:%M %p")
                            ),
                        )

                    completed_challenges.append(challenge)

        conn.close()

        return render_template(
            "user/practice_hub/completed_challenges.html",
            challenges=completed_challenges)
    else:
        return redirect(url_for("auth.login"))

# Route that filters the challenges by the users' Keywprds
@practice_hub_bp.route("/practice-hub/search", methods=["GET"])
def search():
    if "user_id" in session:

        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        cursor.execute("""SELECT challenge_id,
                                number,
                                challenge_title,
                                difficulty_level
                                FROM Challenge""")
        all_challenges = cursor.fetchall()

        filtered_challenges = (
            []
        )  # This will hold the courses that match the search keyword
        if request.method == "GET":
            keyword = request.args.get(
                "search"
                # Gets the keyword entered by the user and converts it to
                # lowercase for case-insensitive search
            ).lower()
            if not keyword == "" and not keyword.isspace():
                for challenge in all_challenges:
                    for word in challenge:
                        word = str(
                            word
                            # Converts each word in the course block to
                            # lowercase for case-insensitive search
                        ).lower()
                        # Checks if the keyword is present in any word of the
                        # course block
                        if (keyword in word):
                            filtered_challenges.append(challenge)
                            break

                return render_template(
                    "user/practice_hub/search_result.html",
                    challenges=filtered_challenges, page_title="Search Result"
                )
            else:
                return redirect(
                    url_for("practice_hub.uncomplete_practice_challenges"))
    else:
        return redirect(url_for("auth.login"))
