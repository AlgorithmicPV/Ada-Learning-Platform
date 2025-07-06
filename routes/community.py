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
import markdown

community_bp = Blueprint("community", __name__)

# All routes check if the user logged in or not
# If the user is not logged in, it redirects to the login page


# Function to get all community questions from the database
# Used a function because I can use this function to get all community
# questions and filter them according to the below routes
def get_all_community_questions_from_db():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT question_id, user_id, question, created_at FROM Question")
    question_details = cursor.fetchall()

    # reverse the whole data come from the database
    # From this latest discussions will show at the top
    # As the new discussions are added at the end of the database
    question_details.reverse()

    # Keeps an empty list to store all the question details
    # Then we can psss this array to client side
    # to render the question cards
    question_cards_detail = []

    for question_detail in question_details:
        posted_user_id = question_detail[1]
        question_id = question_detail[0]

        # Gets the Name and profile image of the user who posted the discussion
        # and Store it in user_data
        cursor.execute(
            "SELECT full_name, profile_image FROM User WHERE user_id=?",
            (posted_user_id,),
        )
        user_data = cursor.fetchall()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Answer WHERE question_id = ?", (question_id,)
        )
        number_of_replies = cursor.fetchone()

        # As the question_detail is a tuple, I used += operator to add the user_data and number_of_replies
        # Because they are also tuples
        question_detail += user_data
        question_detail += number_of_replies

        # Convert the question_detail tuple to a list to modify it easily
        temp_question_detail = list(question_detail)

        today = date.today()

        # Extract the date from the created_at field
        # and format it to compare with today's date
        question_date = question_detail[3].split("T")[0]

        # This helps to check, if the quesiont / discussion is posted today
        # It will show only the time in 12 hour format
        # If not, it will show the date and time in 12 hour format
        # This helps for users to find new discussions easily
        if str(today) == question_date:
            time_str = question_detail[3].split("T")[1]
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
            time_12hr = time_obj.strftime("%I:%M %p")
            temp_question_detail[3] = time_12hr
        else:
            format_string = "%Y-%m-%dT%H:%M:%S"
            temp_question_detail[3] = str(
                (datetime.strptime(question_detail[3], format_string)).strftime(
                    "%Y-%m-%d %I:%M %p"
                )
            )

        user_id = session.get("user_id")

        if question_detail[1] == user_id:
            temp_question_detail[4] = "You"

        # Removes the user_id from the question_detail
        # Because it is not needed for the client side
        temp_question_detail.remove(question_detail[1])

        # As this platform enables to use markdown for user inputs, but for the preview removes the markdown syntax
        # and shows the text only for the better user experience and keeps the
        # same height for each question card
        temp_question_detail[1] = strip_markdown.strip_markdown(
            question_detail[2])

        # Checks if the user has saved this discussion
        # By trying to get a saved_question_id from the Saved_question table where the user_id and question_id matches
        # If there is value for saved_question_id, it means the user has saved that discussion
        # and appends "saved" to the temp_question_detail list if not appends "unsaved"
        # This helps for the frontend to show which icon should be shown for
        # the save button
        cursor.execute(
            "SELECT saved_question_id FROM Saved_question WHERE user_id=? AND question_id=?",
            (user_id, question_id),
        )

        saved_question_id = cursor.fetchone()

        if saved_question_id:
            temp_question_detail.append("saved")
        else:
            temp_question_detail.append("unsaved")

        if question_detail[1] == user_id:
            temp_question_detail.append("you")
        else:
            temp_question_detail.append(" ")

        # Converts the temp_question_detail list back to a tuple
        # Because the question_detail is a tuple and we need to keep the same
        # data type
        question_detail = tuple(temp_question_detail)

        # Appends the question_detail tuple to the question_cards_detail list
        # This list will be returned to the client side
        question_cards_detail.append(question_detail)

    conn.close()
    return question_cards_detail


# Route that displays all community questions that happened in the platform
@community_bp.route("/community")
def all_community_questions():
    if "user_id" in session:
        return render_template(
            "user/community/community_all.html",
        )
    else:
        return redirect(url_for("auth.login"))


# This Route connects with the client side, and each 2500 milliseconds
# it calls the get_all_community_questions function to keep the data updated
@community_bp.route("/community/get-all-questions")
def get_all_community_questions():
    if "user_id" in session:
        question_cards_detail = get_all_community_questions_from_db()
        return jsonify(question_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community questions that happened on one day
@community_bp.route("/community/newest")
def newest_community_questions():
    if "user_id" in session:
        return render_template("user/community/community_new.html")
    else:
        return redirect(url_for("auth.login"))


# This routes also connects with the client side, and in each 2.5 seconds
# It sends the questions that have been posted today
# This helps for the users to find new discussions easily
@community_bp.route("/community/get-new-questions")
def get_new_community_questions():
    if "user_id" in session:
        question_cards_detail = get_all_community_questions_from_db()
        new_question_cards_detail = []
        today = str(date.today())
        for question_card_detail in question_cards_detail:
            posted_date = str(parse(question_card_detail[2])).split(" ")[0]
            if posted_date == today:
                new_question_cards_detail.append(question_card_detail)
        return jsonify(new_question_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Routes that displays all questions that have done by the user
@community_bp.route("/community/you")
def user_community_questions():
    if "user_id" in session:
        return render_template("user/community/community_user.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have been posted by the relevant logged in user
# This helps user to find answers for their questions easily
@community_bp.route("/community/get-user-posted-questions")
def get_user_posted_questions():
    if "user_id" in session:
        question_cards_detail = get_all_community_questions_from_db()
        user_question_cards_detail = []
        for question_card_detail in question_cards_detail:
            if question_card_detail[7] == "you":
                user_question_cards_detail.append(question_card_detail)
        return jsonify(user_question_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community questions that have not been answered
@community_bp.route("/community/unanswered")
def unanswered_community_questions():
    if "user_id" in session:
        return render_template("user/community/community_unanswered.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have not been answered yet
@community_bp.route("/community/get-unanswered-questions")
def get_unanswered_questions():
    if "user_id" in session:
        question_cards_detail = get_all_community_questions_from_db()
        unanswered_question_cards_detail = []
        for question_card_detail in question_cards_detail:
            if question_card_detail[5] == 0:
                unanswered_question_cards_detail.append(question_card_detail)
        return jsonify(unanswered_question_cards_detail)
    else:
        return redirect(url_for("auth.login"))


# Route that displays all community questions that have been saved by the user
@community_bp.route("/community/saved")
def saved_community_questions():
    if "user_id" in session:
        return render_template("user/community/community_saved.html")
    else:
        return redirect(url_for("auth.login"))


# This route connects with the client side, and in each 2.5 seconds
# It sends the questions that have been saved by the user
# This helps to user group questions that they think are important
@community_bp.route("/community/get-saved-questions")
def get_saved_questions():
    if "user_id" in session:
        question_cards_detail = get_all_community_questions_from_db()
        saved_question_cards_detail = []
        for question_card_detail in question_cards_detail:
            if question_card_detail[6] == "saved":
                saved_question_cards_detail.append(question_card_detail)
        return jsonify(saved_question_cards_detail)
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
                question_id = str(uuid.uuid4())
                user_id = session.get("user_id")
                question = user_input
                created_at = datetime.now().isoformat(timespec="seconds")

                cursor.execute(
                    "INSERT INTO Question (question_id, user_id, question, created_at) VALUES (?, ?, ?, ?)",
                    (
                        question_id,
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
            client_question_id = data["questionId"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Valide the question_id coming from the client side with the
            # database
            cursor.execute(
                "SELECT question_id FROM question WHERE question_id = ?",
                (client_question_id,),
            )
            question_id = cursor.fetchone()

            if question_id:
                user_id = session.get("user_id")

                # Ckeck has user saved that discussion
                cursor.execute(
                    "SELECT saved_question_id FROM Saved_question WHERE question_id=? AND user_id=?",
                    (
                        question_id[0],
                        user_id,
                    ),
                )
                saved_question_id_from_db = cursor.fetchone()

                # if user has saved, delete the saved discussion from the saved_question table
                # if user has not saved, insert a new row to the saved_question table
                # and set the isSave variable to "yes" or "no" accordingly,
                # this helps for the frontend to show the correct icon
                if saved_question_id_from_db:
                    cursor.execute(
                        "DELETE FROM Saved_question WHERE saved_question_id=?",
                        (saved_question_id_from_db),
                    )
                    conn.commit()
                    conn.close()

                    is_save = "no"
                else:
                    saved_question_id = str(uuid.uuid4())
                    cursor.execute(
                        "INSERT INTO Saved_question (saved_question_id, question_id, user_id) VALUES (?, ?, ?)",
                        (saved_question_id, question_id[0], user_id),
                    )
                    conn.commit()
                    conn.close()

                    is_save = "yes"
            else:
                print("in valid")

            return jsonify({"isSave": is_save}), 200
    else:
        return redirect(url_for("auth.login"))


# This route shows the all the answers relevant to clicked question
@community_bp.route("/community/<question_id>/discussions")
def discussions(question_id):
    if "user_id" in session:
        # Check linked question_id is same as the session question_id
        # IF it is then it will show the discussion page
        if question_id == session.get("question_id"):
            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            question_details_that_goes_to_client_side = []

            cursor.execute(
                "SELECT user_id, question, created_at FROM Question WHERE question_id=?",
                (question_id,),
            )
            question_details_from_db = cursor.fetchall()[0]

            # If users have types their question using markdown synatx
            # converts them into HTML format
            # and appends to the question_details_that_goes_to_client_side list
            question_details_that_goes_to_client_side.append(
                markdown.markdown(question_details_from_db[1])
            )

            today = date.today()

            # Extract the date from the created_at field
            # and format it to compare with today's date
            question_date = question_details_from_db[2].split("T")[0]

            # This helps to check, if the quesiont / discussion is posted today
            # It will show only the time in 12 hour format
            # If not, it will show the date and time in 12 hour format
            # This helps for users to find new discussions easily
            if str(today) == question_date:
                time_str = question_details_from_db[2].split("T")[1]
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
                time_12hr = time_obj.strftime("%I:%M %p")
                question_details_that_goes_to_client_side.append(time_12hr)
            else:
                format_string = "%Y-%m-%dT%H:%M:%S"
                question_details_that_goes_to_client_side.append(
                    str(
                        (
                            datetime.strptime(
                                question_details_from_db[2], format_string
                            )
                        ).strftime("%Y-%m-%d %I:%M %p")
                    )
                )

            user_id = session.get("user_id")

            # For better user experiences, if the question is posted by the logged in user
            # it will show "You" instead of their name
            if question_details_from_db[0] == user_id:
                question_details_that_goes_to_client_side.append("You")
            else:
                cursor.execute(
                    "SELECT full_name FROM User WHERE user_id=?",
                    (question_details_from_db[0],),
                )
                posted_user_name = cursor.fetchone()[0]
                question_details_that_goes_to_client_side.append(
                    posted_user_name)

            # Append the profile image of the user who posted the question
            cursor.execute(
                "SELECT profile_image FROM User WHERE user_id = ?",
                (question_details_from_db[0],),
            )
            profile_image = cursor.fetchone()[0]
            question_details_that_goes_to_client_side.append(profile_image)

            # Check has the user saved this discussion
            # depending on that append "saved" or "unsaved" to the question_details_that_goes_to_client_side list
            # This helps for the frontend to show the correct icon
            cursor.execute(
                "SELECT saved_question_id FROM Saved_question WHERE user_id=? AND question_id=?",
                (user_id, question_id),
            )

            saved_question_id = cursor.fetchone()

            if saved_question_id:
                question_details_that_goes_to_client_side.append("saved")
            else:
                question_details_that_goes_to_client_side.append("unsaved")

            # Counts the number of replies for the question and appends it to
            # the question_details_that_goes_to_client_side list
            cursor.execute(
                "SELECT COUNT(*) FROM Answer WHERE question_id = ?", (question_id,)
            )
            number_of_replies = cursor.fetchone()[0]
            question_details_that_goes_to_client_side.append(number_of_replies)

            # Appends question_id to the question_details_that_goes_to_client_side list
            # This helps to toggle the save and unsave functionality
            question_details_that_goes_to_client_side.append(question_id)

            return render_template(
                "user/community/discussions.html",
                question_detail=question_details_that_goes_to_client_side,
            )
    else:
        return redirect(url_for("auth.login"))


@community_bp.route("/community/get-answers", methods=["POST"])
def get_answers():
    if "user_id" in session:
        if request.is_json:
            data = request.get_json()
            client_question_id = data["questionId"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Valide the question_id coming from the client side with the
            # database
            cursor.execute(
                "SELECT question_id FROM question WHERE question_id = ?",
                (client_question_id,),
            )
            question_id = cursor.fetchone()

            if question_id:
                session["question_id"] = client_question_id
                redirect_url = url_for(
                    "community.discussions", question_id=client_question_id
                )
                return jsonify({"redirect_url": redirect_url})
    else:
        return redirect(url_for("auth.login"))


# Route that adds answers to the relevant question
@community_bp.route("/community/add-answers", methods=["POST"])
def add_answers():
    if "user_id" in session:
        pass
    else:
        return redirect(url_for("auth.login"))
