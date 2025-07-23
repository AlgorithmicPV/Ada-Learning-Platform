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
import emoji
import string

community_bp = Blueprint("community", __name__)

# All routes check if the user logged in or not
# If the user is not logged in, it redirects to the login page


def to_iso_datetime(input_str, fallback_date=None):
    if fallback_date is None:
        fallback_date = date.today()

    try:
        dt = parse(input_str, default=datetime.combine(fallback_date, datetime.min.time()))
    except Exception as e:
        raise ValueError(f"Invalid time format: {input_str}") from e

    return dt.strftime("%Y-%m-%dT%H:%M:%S")

# I Use a function because I can use this function to get all community
# questions and filter them according to the below routes
def get_community_questions_from_db(filter_query):
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    user_id = session.get("user_id")
    static_base = url_for('static', filename='')
    base_query = f"""
            SELECT
                Q.question_id,
                Q.question,
                /*
                This helps to check, if the quesiont / discussion is posted today
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
                    WHEN U.auth_provider = 'manual' THEN :static_base || U.profile_image
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
    cursor.execute( base_query + filter_query + grouping_and_ordering_query, {"uid" : user_id, "static_base": static_base})
    question_cards_detail_from_db = cursor.fetchall()
    last_question_id = question_cards_detail_from_db[0][0]
    conn.close()
    if question_cards_detail_from_db: 
            question_cards_detail = []
            for question_card in question_cards_detail_from_db:
                temp_list = list(question_card)
                temp_list[1] = strip_markdown.strip_markdown(question_card[1])
                question_cards_detail.append(temp_list)
            return question_cards_detail
    else:
        return ""
    
def get_new_community_questions_from_db():
    pass


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
        question_cards_detail = get_community_questions_from_db("")
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
        new_question_cards_detail = get_community_questions_from_db("WHERE  DATE(Q.created_at) = DATE('now')")
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
        user_question_cards_detail = get_community_questions_from_db("WHERE Q.user_id = :uid")
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
        unanswered_question_cards_detail = get_community_questions_from_db("WHERE A.answer_id IS NULL")
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
        saved_question_cards_detail = get_community_questions_from_db(
            """
            WHERE EXISTS (
            SELECT 1
            FROM Saved_question SQ
            WHERE SQ.question_id = Q.question_id
                AND SQ.user_id = :uid
            )
            """)
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
                    """
                    INSERT 
                    INTO Question (question_id, 
                                    user_id, 
                                    question, 
                                    created_at) 
                    VALUES (?, ?, ?, ?)""",
                    (question_id,
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
                    (question_id[0],
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
        if question_id == session.get("question_id"):
            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()
            user_id = session.get("user_id")
            static_base = url_for('static', filename='') 
            cursor.execute(
                        """
                        SELECT
                            Q.question_id,
                            Q.question,
                            /*
                            This helps to check, if the quesiont / discussion is posted today
                            It will show only the time in 12 hour format
                            If not, it will show the date and time in 12 hour format
                            This helps for users to find new discussions easily 
                            */
                            CASE 
                                WHEN DATE(Q.created_at) = DATE('now')
                                THEN STRFTIME('%I:%M %p', TIME(REPLACE(Q.created_at, 'T', ' '))) 
                                ELSE STRFTIME('%Y-%m-%d %I:%M %p', REPLACE(Q.created_at, 'T', ' ')) 
                            END AS created_at,
                            CASE 
                                WHEN U.user_id = :uid THEN 'You' 
                                ELSE U.full_name
                            END AS posted_user,
                            CASE 
                                WHEN U.auth_provider = 'manual' THEN :static_base || U.profile_image
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
                        """, {"uid": user_id, "qid" : question_id, "static_base":static_base})
            question_details_from_db = cursor.fetchall()
            if question_details_from_db:
                question_details_that_goes_to_client_side = list(question_details_from_db[0])
                question_details_that_goes_to_client_side[1] = markdown.markdown(question_details_that_goes_to_client_side[1],extensions=['fenced_code'])
                return render_template(
                    "user/community/discussions.html",
                    question_detail=question_details_that_goes_to_client_side,
                )
            else:
                return redirect(url_for("community.all_community_questions"))
        else:
            return redirect(url_for("community.all_community_questions"))
    else:
        return redirect(url_for("auth.login"))


# This Route validates the question_id coming from the client side with the database question_id
# It passes the redirect url to the client side to change the page
@community_bp.route("/community/check-qid", methods=["POST"])
def check_qid():
    if "user_id" in session:
        if request.is_json:
            data = request.get_json()
            client_question_id = data["questionId"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Uses the client side question id to check if there is an actual question id in the database
            # If there is a question id in the database, it will set the
            # session question_id
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
        if request.is_json:
            data = request.get_json()
            user_answer = data["userAnswer"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Before adding to the database, check userinput is not a blank or
            # empty string
            if not user_answer == "" and not user_answer.isspace():
                created_at = datetime.now().isoformat(timespec="seconds")
                answer_id = str(uuid.uuid4())
                question_id = session.get("question_id")
                user_id = session.get("user_id")
                cursor.execute("""
                               INSERT 
                               INTO Answer
                               (answer_id, 
                               question_id, 
                               user_id, 
                               content, 
                               created_at)
                               VALUES (?, ?, ?, ?, ?)""",
                               (answer_id, 
                                question_id, 
                                user_id, 
                                user_answer, 
                                created_at))

                conn.commit()
                conn.close()

            return "", 200
    else:
        return redirect(url_for("auth.login"))

# This route gets all the answers that are relevant to the question that user clicked
# THis route passes the answers to the client side in every 2.5 seconds
# To keep anwers updated


@community_bp.route("/community/get-answers")
def get_answers():
    if "user_id" in session:
        question_id = session.get("question_id")

        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        static_base = url_for('static', filename='') 

        user_id = session.get("user_id")

        cursor.execute(
            """
            SELECT 
                A.answer_id,
                A.content,
                CASE 
                WHEN DATE(A.created_at) = DATE('now')
                    THEN STRFTIME('%I:%M %p', TIME(REPLACE(A.created_at, 'T', ' '))) 
                    ELSE STRFTIME('%Y-%m-%d %I:%M %p', REPLACE(A.created_at, 'T', ' ')) 
                END AS created_at,
                CASE 
                WHEN U.user_id = :uid THEN 'You' 
                    ELSE U.full_name
                END AS answered_user,
                CASE 
                WHEN U.auth_provider = 'manual' THEN :static_base || U.profile_image
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
            GROUP BY A.answer_id
        """, {"uid": user_id, "qid": question_id, "static_base": static_base})

        answers_details_that_go_to_the_frontend = cursor.fetchall()
        return jsonify(answers_details_that_go_to_the_frontend)
    else:
        return redirect(url_for("auth.login"))

# This route handles the like and unlike functionality of the answers
# If user has likes the answer it will comver to unlike and other way around
# It also counts the number of likes for the answer and sends it to the
# client side


@community_bp.route("/community/toggle-like", methods=["POST"])
def toggle_like():
    if "user_id" in session:
        if request.is_json:
            data = request.get_json()
            client_answer_id = data["answerId"]

            conn = sqlite3.connect("database/app.db")
            cursor = conn.cursor()

            # Validates the answer_id coming from the client side with the database
            # If there is an answer_id in the database, it will proceed with the like/unlike functionality
            # and count the number of likes for that answer
            cursor.execute(
                "SELECT answer_id FROM Answer WHERE answer_id=?", (client_answer_id,))
            answer_id = cursor.fetchone()

            if answer_id:
                user_id = session.get("user_id")

                cursor.execute(
                    "SELECT like_id FROM AnswerLike WHERE user_id=? AND answer_id=?",
                    (user_id,
                     client_answer_id,
                     ))
                liked_answer_id_from_db = cursor.fetchone()

                # if the liked_answer_id has some kind of value it will delete from the AnswerLike table,
                # and set the like variable to "no"
                # IF there is no value in the liked_answer_id_from_db,
                # It will insert the new like answers details to the AnswerLike table
                # and set the like variable to "yes"
                if liked_answer_id_from_db:
                    cursor.execute(
                        "DELETE FROM AnswerLike WHERE like_id=?",
                        (liked_answer_id_from_db))
                    conn.commit()
                    like = "no"
                else:
                    like_id = str(uuid.uuid4())
                    cursor.execute(
                        "INSERT INTO AnswerLike (like_id, user_id, answer_id) VALUES (?, ?, ?)",
                        (like_id,
                         user_id,
                         client_answer_id))
                    conn.commit()
                    like = "yes"

                # Counts the number of likes for the answer
                # and sends it to the client side
                cursor.execute("""
                            SELECT COUNT(*) FROM AnswerLike WHERE answer_id=?
                           """, (client_answer_id,))
                number_of_likes = cursor.fetchone()[0]
                conn.close()
            else:
                print("not valid")

            return jsonify({"like": like, "nu_likes": number_of_likes}), 200
    else:
        return redirect(url_for("auth.login"))

# This route gets the number of answers for the relevant question
# This has connected with the client side, and pass data in every 2.5 seconds
# to keep the number of answers updated


@community_bp.route("/community/get-number-of-answers")
def get_number_of_answers():
    if "user_id" in session:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()

        question_id = session.get("question_id")

        cursor.execute(
            "SELECT COUNT(*) FROM Answer WHERE question_id = ?", (question_id,)
        )
        number_of_answers = cursor.fetchone()

        return jsonify({"numberOfAnswers": number_of_answers})
    else:
        return redirect(url_for("auth.login"))


# Removes the punctuations of a text
translator = str.maketrans('', '', string.punctuation)

# This route filters the questions based on the user's keywords
# This route will only work if the keyword is not empty or just whitespace


@community_bp.route("/community/search/", methods=["GET"])
def search_questions():
    if "user_id" in session:
        if request.method == "GET":
            keyword = request.args.get("search")
            search_result = []
            if not keyword == "" and not keyword.isspace():
                question_cards_detail = get_community_questions_from_db("")
                for question_card_detail in question_cards_detail:

                    # Converts the question from the database to plain text
                    # This makes it easier to convert into a flat array
                    flat_question = question_card_detail[1].replace(
                        '\r\n', ' ').replace('\n', ' ')

                    # Removes existing emojis, otherwise, the algorithm doesn't work properly
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
                    # And save the array that has small number of elements to a varaible called denominator
                    # This is done because, if we use the bigger value, our percentage will be getting lower
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

                    # If the percentage is increased than 50 append to the search_result array
                    # I chose 50 because it is a fair value and the center of
                    # 100
                    if percentage_of_equility >= 50:
                        search_result.append(question_card_detail)

                return render_template(
                    "user/community/community_search_result.html",
                    search_result=search_result)
            else:
                return redirect(url_for("community.all_community_questions"))
    else:
        return redirect(url_for("auth.login"))
