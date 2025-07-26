from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3
from datetime import datetime, timedelta, date
from utils import divide_array_into_chunks

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("user_id"):
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        user_id = session.get("user_id")
        cursor.execute(
            """
            SELECT
                U.user_id,
                U.full_name,
                C.course_name,
                C.course_id,

                -- First lesson the user hasn't done yet in the current course
                (
                    SELECT L.lesson_title
                    FROM Lesson L
                    WHERE L.course_id = C.course_id
                    AND NOT EXISTS (
                        SELECT 1
                        FROM User_lesson UL
                        WHERE UL.lesson_id = L.lesson_id
                            AND UL.user_id = U.user_id
                    )
                    ORDER BY L.lesson_order ASC
                    LIMIT 1
                ) AS lesson_name,

                -- Same as above but returning lesson_id
                (
                    SELECT L.lesson_id
                    FROM Lesson L
                    WHERE L.course_id = C.course_id
                    AND NOT EXISTS (
                        SELECT 1
                        FROM User_lesson UL
                        WHERE UL.lesson_id = L.lesson_id
                            AND UL.user_id = U.user_id
                    )
                    ORDER BY L.lesson_order ASC
                    LIMIT 1
                ) AS lesson_id,

                -- Course progress: how many lessons completed / total lessons
                (
                    SELECT ROUND(
                        100.0 * COUNT(UL.lesson_id) /
                        NULLIF((SELECT COUNT(*) FROM Lesson L2 WHERE L2.course_id = C.course_id), 0)
                    )
                    FROM User_lesson UL
                    JOIN Lesson L3 ON UL.lesson_id = L3.lesson_id
                    WHERE UL.user_id = U.user_id
                    AND L3.course_id = C.course_id
                    AND UL.status = 'completed'
                ) AS percentage_of_the_course,

                -- Challenge progress: total completed vs total
                (
                    SELECT ROUND(
                        100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM Challenge), 0)
                    )
                    FROM Challenge_attempt
                    WHERE user_id = U.user_id AND status = 'Completed'
                ) AS completed_challenge_percentage,

                -- Total completed challenges
                (
                    SELECT COUNT(*)
                    FROM Challenge_attempt
                    WHERE user_id = U.user_id AND status = 'Completed'
                ) AS completed_challenges_amount,

                -- Most answered question by all users
                (
                    SELECT Q.question
                    FROM Question Q
                    LEFT JOIN Answer A ON A.question_id = Q.question_id
                    GROUP BY Q.question_id
                    ORDER BY COUNT(A.answer_id) DESC
                    LIMIT 1
                ) AS top_question,

                -- ID of the most answered question
                (
                    SELECT Q.question_id
                    FROM Question Q
                    LEFT JOIN Answer A ON A.question_id = Q.question_id
                    GROUP BY Q.question_id
                    ORDER BY COUNT(A.answer_id) DESC
                    LIMIT 1
                ) AS top_question_id,

                -- List of all activity dates (lessons, answers, questions, etc.)
                (
                    SELECT
                        GROUP_CONCAT(DISTINCT DATE(dt) ORDER BY DATE(dt) DESC)
                    FROM (
                        SELECT AR.generated_at AS dt FROM Ai_resource AR WHERE AR.user_id = U.user_id
                        UNION
                        SELECT A.created_at FROM Answer A WHERE A.user_id = U.user_id
                        UNION
                        SELECT CA.completed_at FROM Challenge_attempt CA WHERE CA.user_id = U.user_id
                        UNION
                        SELECT E.enrolled_at FROM Enrollment E WHERE E.user_id = U.user_id
                        UNION
                        SELECT E.last_accessed FROM Enrollment E WHERE E.user_id = U.user_id
                        UNION
                        SELECT Q.created_at FROM Question Q WHERE Q.user_id = U.user_id
                        UNION
                        SELECT UL.completed_at FROM User_lesson UL WHERE UL.user_id = U.user_id
                        UNION
                        SELECT U2.join_date FROM User U2 WHERE U2.user_id = U.user_id
                    ) AS combined_dates
                ) AS all_available_dates,

                -- 1 coin per 5 easy challenges completed
                CAST(ROUND(1.0 * (
                    SELECT COUNT(*)
                    FROM Challenge C
                    JOIN Challenge_attempt CA ON CA.challenge_id = C.challenge_id
                    WHERE CA.user_id = :uid
                    AND CA.status = 'Completed'
                    AND C.difficulty_level = 'Easy'
                ) / 5) AS INTEGER) AS bronze_coins,


                -- 1 coin per 5 medium challenges
                CAST(ROUND(1.0 * (
                    SELECT COUNT(*)
                    FROM Challenge C
                    JOIN Challenge_attempt CA ON CA.challenge_id = C.challenge_id
                    WHERE CA.user_id = :uid
                    AND CA.status = 'Completed'
                    AND C.difficulty_level = 'Medium'
                ) / 5) AS INTEGER) AS silver_coins,

                -- 1 coin per 5 hard challenges
                CAST(ROUND(1.0 * (
                    SELECT COUNT(*)
                    FROM Challenge C
                    JOIN Challenge_attempt CA ON CA.challenge_id = C.challenge_id
                    WHERE CA.user_id = :uid
                    AND CA.status = 'Completed'
                    AND C.difficulty_level = 'Hard'
                ) / 5) AS INTEGER) AS gold_coins,

                -- Leaderboard formatted like a JSON array (top 5 users by challenge completion)
                (
                    SELECT
                        GROUP_CONCAT(name || ', ' || completed, ', ')
                    FROM (
                        SELECT
                            U2.full_name AS name,
                            COUNT(CA.id) AS completed
                        FROM User U2
                        JOIN Challenge_attempt CA ON CA.user_id = U2.user_id AND CA.status = 'Completed'
                        GROUP BY U2.user_id
                        ORDER BY completed DESC
                        LIMIT 5
                    )
                ) AS lead_board

            FROM User U
            LEFT JOIN (
                -- Get the latest started enrollment for the user
                SELECT E1.*
                FROM Enrollment E1
                WHERE E1.status = 'started'
                AND DATETIME(REPLACE(E1.last_accessed, 'T', ' ')) = (
                    SELECT MAX(DATETIME(REPLACE(E2.last_accessed, 'T', ' ')))
                    FROM Enrollment E2
                    WHERE E2.user_id = :uid
                    AND E2.status = 'started'
                )
            ) E ON E.user_id = U.user_id
            LEFT JOIN Course C ON C.course_id = E.course_id
            WHERE U.user_id = :uid
            GROUP BY U.user_id, C.course_id;

            """, {'uid': user_id})

        dashboard_data_from_db = cursor.fetchall()

        print(session.get('lesson_id'))

        dashboard_data = dashboard_data_from_db[0]

        if dashboard_data[3]:
            session['course_id'] = dashboard_data[3]
            session["lesson_id"] = dashboard_data[5]

        if dashboard_data[10]:
            session["question_id"] = dashboard_data[10]

        str_dates = dashboard_data[11].split(',')

        dates_obj = []

        # The database output is a string
        # Convert it into a list (array) for further processing
        for str_date in str_dates:
            date_obj = datetime.strptime(str_date, "%Y-%m-%d").date()
            dates_obj.append(date_obj)

        dates_obj.append(date.today().isoformat())

        number_of_dates = len(dates_obj)

        streak = 0

        # If the number of dates is more than 1
        # Check if the next date is equal to the current date minus 1
        # Note: all the dates are in descending order
        # If it is true, add 1 to the streak
        if number_of_dates > 1:
            for i in range(number_of_dates):
                if dates_obj[i + 1] == dates_obj[i] - timedelta(days=1):
                    streak = streak + 1
                else:
                    break

        leadboard_from_db = dashboard_data[15]
        leadboard = ""
        if leadboard_from_db:
            leadboard = leadboard_from_db.split(',')
            leadboard = divide_array_into_chunks(leadboard, 2)

        return render_template("user/dashboard.html",
                               dashboard_data=dashboard_data,
                               streak=streak,
                               leadboard=leadboard)
    else:
        return redirect(url_for("auth.login"))
