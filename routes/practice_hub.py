from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

practice_hub_bp = Blueprint("practice_hub", __name__)


@practice_hub_bp.route("/practice-hub", methods=["GET", "POST"])
def uncomplete_practice_questions():
    if session.get("username"):
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        cursor.execute("SELECT challenge_id FROM Challenge")
        all_challenges_ids = cursor.fetchall()

        # print(all_challenges_ids)
        for challenge_id in all_challenges_ids:
            # print(challenge_id[0])
            cursor.execute("""
                           SELECT status 
                           FROM Challenge_attempt 
                           WHERE challenge_id=?""", (challenge_id[0],))

            status = cursor.fetchone()
            if status == None:
                print("havent Started")

        page_title = "Unsolved"
        return render_template("user/practice_hub/questions.html", page_title=page_title)
    else:
        return redirect(url_for("auth.login"))
