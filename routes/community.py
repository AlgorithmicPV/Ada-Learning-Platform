from flask import Blueprint, session, redirect, url_for, request, jsonify, render_template
import sqlite3
import uuid
from datetime import datetime, date

community_bp = Blueprint("community", __name__)

# Route that displays all community discussions that happened in the platform


@community_bp.route("/community")
def all_community_discussion():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()


        cursor.execute("SELECT chat_id, user_id, question, created_at FROM Chat")
        chat_details = cursor.fetchall()

        chat_cards_detail = []

        

        for chat_detail in chat_details:
            user_id = chat_detail[1]
            chat_id = chat_detail[0]

            cursor.execute("SELECT full_name, profile_image FROM User WHERE user_id=?", (user_id,))
            user_data = cursor.fetchall()[0]


            cursor.execute("SELECT COUNT(*) FROM Reply WHERE chat_id = ?", (chat_id,))
            number_of_replies = cursor.fetchone()

            chat_detail += user_data
            chat_detail += number_of_replies

            temp_chat_detail = list(chat_detail)

            today = date.today()
            chat_date = (chat_detail[3].split("T")[0])
            if str(today) == chat_date:
                time_str = chat_detail[3].split("T")[1]
                time_obj = datetime.strptime(time_str, '%H:%M:%S')
                time_12hr = time_obj.strftime('%I:%M %p')
                temp_chat_detail[3] = time_12hr
            else:
                temp_chat_detail[3] = chat_date
            
            chat_detail = tuple(temp_chat_detail)

            chat_cards_detail.append(chat_detail)

        return render_template("user/community/community_all.html", chat_cards_detail = chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that happened on one day


@community_bp.route("/community/newest")
def newest_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Routes that displays all discussion that have done by the user


@community_bp.route("/community/you")
def your_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that have not been answered


@community_bp.route("/community/unanswered")
def unanswered_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that have been saved by the user


@community_bp.route("/community/saved")
def saved_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))


@community_bp.route("/community/add-new-post", methods=["POST"])
def add_new_post():
    if "user_id" in session:
        if request.method == "POST":
            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            user_input = request.form.get("user-question-input")

            chat_id = str(uuid.uuid4())
            user_id = session.get("user_id")
            question = user_input
            created_at = datetime.now().isoformat(timespec="seconds")

            cursor.execute("INSERT INTO Chat (chat_id, user_id, question, created_at) VALUES (?, ?, ?, ?)",
                           (chat_id, user_id, question, created_at,))
            conn.commit()
            conn.close()

            return redirect(url_for("community.all_community_discussion"))
    else:
        return redirect(url_for("auth.login"))
