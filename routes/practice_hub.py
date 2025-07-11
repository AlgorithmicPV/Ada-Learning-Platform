from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import sqlite3
import uuid
import datetime
import markdown

practice_hub_bp = Blueprint("practice_hub", __name__)


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

        for challenge in all_challenges:
            cursor.execute("""
                          SELECT status
                           FROM Challenge_attempt
                           WHERE challenge_id=? AND
                           user_id=?""", (challenge[0], user_id,))

            status = cursor.fetchone()
            if status == None:
                challenge += ("-",)
                unsolved_challenges.append(challenge)

            if status:
                if status[0] == "Started":
                    challenge += ("Started",)
                    unsolved_challenges.append(challenge)

        page_title = "Unsolved"
        conn.close()
        return render_template("user/practice_hub/challenges.html", page_title=page_title, challenges=unsolved_challenges)
    else:
        return redirect(url_for("auth.login"))


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
                if status == None:
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
                formated_challenge_title = challenge_title.replace(" ", "-")

                return redirect(url_for("practice_hub.show_challenge", challenge_title=formated_challenge_title))
            else:
                return redirect(url_for("practice_hub.uncomplete_practice_challenges"))

        else:
            return redirect(url_for("practice_hub.uncomplete_practice_challenges"))
    else:
        return redirect(url_for("auth.login"))


@practice_hub_bp.route("/practice-hub/<challenge_title>")
def show_challenge(challenge_title):
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

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

        return render_template("user/practice_hub/challenge.html", challenge_info=challenge_info_list)
    else:
        return redirect(url_for("auth.login"))

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
                answer = markdown.markdown(cursor.fetchone()[0],extensions=['fenced_code'])
                print(answer)
                return jsonify({"answer":answer})
    else:
        return redirect(url_for("auth.login"))

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
                answer = markdown.markdown(cursor.fetchone()[0],extensions=['fenced_code'])
                
                cursor.execute("""
                    SELECT 
                    challenge_title
                    FROM Challenge WHERE challenge_id=?
                    """, (client_challenge_id,))
                
                title = cursor.fetchone()[0]

                output = {
                    "answer":answer,
                    "title":title
                }
                
                return jsonify(output)
    else:
        return redirect(url_for("auth.login"))


@practice_hub_bp.route("/practice-hub/completed", methods=["POST"])
def completed():
    if "user_id" in session:
        pass