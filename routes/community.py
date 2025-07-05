from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    request,
    jsonify,
    render_template,
)
import sqlite3
import uuid
from datetime import datetime, date
import strip_markdown
from dateutil.parser import parse

community_bp = Blueprint("community", __name__)

# All routes check if the user logged in or not
# If the user is not logged in, it redirects to the login page


# Function to get all community discussions from the database
# Used a function because I can use this function to get all community discussions and filter them according to the below routes
def get_all_community_discussions_from_db():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT chat_id, user_id, question, created_at FROM Chat")
    chat_details = cursor.fetchall()

    # reverse the whole data come from the database
    # From this latest discussions will show at the top
    # As the new discussions are added at the end of the database
    chat_details.reverse()

    # Keeps an empty list to store all the chat details
    # Then we can psss this array to client side
    # to render the chat cards
    chat_cards_detail = []

    for chat_detail in chat_details:
        posted_user_id = chat_detail[1]
        chat_id = chat_detail[0]

        # Gets the Name and profile image of the user who posted the discussion
        # and Store it in user_data
        cursor.execute(
            "SELECT full_name, profile_image FROM User WHERE user_id=?",
            (posted_user_id,),
        )
        user_data = cursor.fetchall()[0]

        cursor.execute("SELECT COUNT(*) FROM Reply WHERE chat_id = ?", (chat_id,))
        number_of_replies = cursor.fetchone()

        # As the chat_detail is a tuple, I used += operator to add the user_data and number_of_replies
        # Because they are also tuples
        chat_detail += user_data
        chat_detail += number_of_replies

        # Convert the chat_detail tuple to a list to modify it easily
        temp_chat_detail = list(chat_detail)

        today = date.today()

        # Extract the date from the created_at field
        # and format it to compare with today's date
        chat_date = chat_detail[3].split("T")[0]

        # This helps to check, if the quesiont / discussion is posted today
        # It will show only the time in 12 hour format
        # If not, it will show the date and time in 12 hour format
        # This helps for users to find new discussions easily
        if str(today) == chat_date:
            time_str = chat_detail[3].split("T")[1]
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
            time_12hr = time_obj.strftime("%I:%M %p")
            temp_chat_detail[3] = time_12hr
        else:
            format_string = "%Y-%m-%dT%H:%M:%S"
            temp_chat_detail[3] = str(
                (datetime.strptime(chat_detail[3], format_string)).strftime(
                    "%Y-%m-%d %I:%M %p"
                )
            )

        # Removes the user_id from the chat_detail
        # Because it is not needed for the client side
        temp_chat_detail.remove(chat_detail[1])

        # As this platform enables to use markdown for user inputs, but for the preview removes the markdown syntax
        # and shows the text only for the better user experience and keeps the same height for each chat card
        temp_chat_detail[1] = strip_markdown.strip_markdown(chat_detail[2])

        user_id = session.get("user_id")

        # Checks if the user has saved this discussion
        # By trying to get a saved_chat_id from the Saved_chat table where the user_id and chat_id matches
        # If there is value for saved_chat_id, it means the user has saved that discussion
        # and appends "saved" to the temp_chat_detail list if not appends "unsaved"
        # This helps for the frontend to show which icon should be shown for the save button
        cursor.execute(
            "SELECT saved_chat_id FROM Saved_chat WHERE user_id=? AND chat_id=?",
            (user_id, chat_id),
        )

        saved_chat_id = cursor.fetchone()

        if saved_chat_id:
            temp_chat_detail.append("saved")
        else:
            temp_chat_detail.append("unsaved")

        if chat_detail[1] == user_id:
            temp_chat_detail.append("you")
        else:
            temp_chat_detail.append(" ")

        # Converts the temp_chat_detail list back to a tuple
        # Because the chat_detail is a tuple and we need to keep the same data type
        chat_detail = tuple(temp_chat_detail)

        # Appends the chat_detail tuple to the chat_cards_detail list
        # This list will be returned to the client side
        chat_cards_detail.append(chat_detail)

    conn.close()
    return chat_cards_detail


# Route that displays all community discussions that happened in the platform
@community_bp.route("/community")
def all_community_discussion():
    if "user_id" in session:
        return render_template(
            "user/community/community_all.html",
        )
    else:
        return redirect(url_for("auth.login"))


# This Route connects with the client side, and each 2500 milliseconds
# it calls the get_all_community_discussion function to keep the data updated
@community_bp.route("/community/get-all-discussion")
def get_all_community_discussion():
    if "user_id" in session:
        chat_cards_detail = get_all_community_discussions_from_db()
        return jsonify(chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community discussions that happened on one day
@community_bp.route("/community/newest")
def newest_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_new.html")
    else:
        return redirect(url_for("auth.login"))


# This routes also connects with the client side, and in each 2.5 seconds
# It sends the discussions that have been posted today
# This helps for the users to find new discussions easily
@community_bp.route("/community/get-new-discussions")
def get_new_community_discussions():
    if "user_id" in session:
        chat_cards_detail = get_all_community_discussions_from_db()
        new_chat_cards_detail = []
        today = str(date.today())
        for chat_card_detail in chat_cards_detail:
            posted_date = str(parse(chat_card_detail[2])).split(" ")[0]
            if posted_date == today:
                new_chat_cards_detail.append(chat_card_detail)
        return jsonify(new_chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Routes that displays all discussion that have done by the user
@community_bp.route("/community/you")
def user_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_user.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the discussions that have been posted by the relevant logged in user
# This helps user to find answers for their questions easily
@community_bp.route("/community/get-user-posted-discussions")
def get_user_posted_discussions():
    if "user_id" in session:
        chat_cards_detail = get_all_community_discussions_from_db()
        user_chat_cards_detail = []
        for chat_card_detail in chat_cards_detail:
            if chat_card_detail[7] == "you":
                user_chat_cards_detail.append(chat_card_detail)
        return jsonify(user_chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community discussions that have not been answered
@community_bp.route("/community/unanswered")
def unanswered_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_unanswered.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the discussions that have not been answered yet
@community_bp.route("/community/get-unanswered-discussions")
def get_unanswered_discussions():
    if "user_id" in session:
        chat_cards_detail = get_all_community_discussions_from_db()
        unanswered_chat_cards_detail = []
        for chat_card_detail in chat_cards_detail:
            if chat_card_detail[5] == 0:
                unanswered_chat_cards_detail.append(chat_card_detail)
        return jsonify(unanswered_chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community discussions that have been saved by the user
@community_bp.route("/community/saved")
def saved_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_saved.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the discussions that have been saved by the user
# This helps to user group discussions that they think are important
@community_bp.route("/community/get-saved-discussions")
def get_saved_discussions():
    if "user_id" in session:
        chat_cards_detail = get_all_community_discussions_from_db()
        saved_chat_cards_detail = []
        for chat_card_detail in chat_cards_detail:
            if chat_card_detail[6] == "saved":
                saved_chat_cards_detail.append(chat_card_detail)
        return jsonify(saved_chat_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route the adds a new post to the community
@community_bp.route("/community/add-new-post", methods=["POST"])
def add_new_post():
    if "user_id" in session:
        if request.is_json:
            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            data = request.json

            user_input = data.get("userQuestionInput")

            # Check the validity of the user input, if it is not empty save to the database
            # If it is empty, do not save to the database
            if user_input.strip() != "":
                chat_id = str(uuid.uuid4())
                user_id = session.get("user_id")
                question = user_input
                created_at = datetime.now().isoformat(timespec="seconds")

                cursor.execute(
                    "INSERT INTO Chat (chat_id, user_id, question, created_at) VALUES (?, ?, ?, ?)",
                    (
                        chat_id,
                        user_id,
                        question,
                        created_at,
                    ),
                )
                conn.commit()
                conn.close()

                return "", 204
    else:
        return redirect(url_for("auth.login"))


# Route the handles the save and unsave functionality of a discussion
@community_bp.route("/community/toggle-save", methods=["POST"])
def toggle_save():
    if "user_id" in session:
        if request.is_json:
            data = request.get_json()
            client_chat_id = data["chatId"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Valide the chat_id coming from the client side with the database
            cursor.execute(
                "SELECT chat_id FROM Chat WHERE chat_id = ?", (client_chat_id,)
            )
            chat_id = cursor.fetchone()

            if chat_id:
                user_id = session.get("user_id")

                # Ckeck has user saved that discussion
                cursor.execute(
                    "SELECT saved_chat_id FROM Saved_chat WHERE chat_id=? AND user_id=?",
                    (
                        chat_id[0],
                        user_id,
                    ),
                )
                saved_chat_id_from_db = cursor.fetchone()

                # if user has saved, delete the saved discussion from the saved_chat table
                # if user has not saved, insert a new row to the saved_chat table
                # and set the isSave variable to "yes" or "no" accordingly, this helps for the frontend to show the correct icon
                if saved_chat_id_from_db:
                    cursor.execute(
                        "DELETE FROM Saved_chat WHERE saved_chat_id=?",
                        (saved_chat_id_from_db),
                    )
                    conn.commit()
                    conn.close()

                    is_save = "no"
                else:
                    saved_chat_id = str(uuid.uuid4())
                    cursor.execute(
                        "INSERT INTO Saved_chat (saved_chat_id, chat_id, user_id) VALUES (?, ?, ?)",
                        (saved_chat_id, chat_id[0], user_id),
                    )
                    conn.commit()
                    conn.close()

                    is_save = "yes"
            else:
                print("in valid")

            return jsonify({"isSave": is_save}), 200
    else:
        return redirect(url_for("auth.login"))
