from flask import Blueprint, session, redirect, url_for, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3
from datetime import datetime, date

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

ai_chat_bp = Blueprint("ai_chat", __name__)


# AI Chat Route
@ai_chat_bp.route("/ai-chat", methods=["GET", "POST"])
def chat():
    if "user_id" in session:
        if request.is_json and request.method == "POST":
            language = session.get("language")
            user_code = session.get("user_code")
            data = request.get_json()
            user_input = data.get("user_input")
            code_output = session.get("output_of_code")
            del session['output_of_code']
            del session["user_code"]
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI assistant built into the Ada Learning Platform, created by G. A. Pasindu Vidunitha. Your role is to help users learn and understand {language} by providing clear and concise explanations. If they ask questions about their written program—such as {user_code} and the output they received {code_output}—respond with simple, direct answers without unnecessary detail.",
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    },
                ],
                temperature=1,
                top_p=1,
                model=model,
            )
            return jsonify(
                {"response": response.choices[0].message.content}), 200
        else:
            return jsonify({"error": "Invalid JSON"}), 400
    else:
        return redirect(url_for("auth.login"))


@ai_chat_bp.route("/ai-course-chat", methods=["GET", "POST"])
def ai_course_chat():
    if "user_id" in session:
        if request.is_json and request.method == "POST":
            data = request.get_json()
            user_input = data.get("user_input")
            ai_course_topic = session.get("ai_course_topic")
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI assistant built into the Ada Learning Platform, created by G. A. Pasindu Vidunitha.This platform helps users learn new programming languages. Your role is to assist learners by providing clear, concise, and accurate explanations related to {ai_course_topic}.",
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    },
                ],
                temperature=1,
                top_p=1,
                model=model,
            )
            return jsonify(
                {"response": response.choices[0].message.content}), 200
        else:
            return jsonify({"error": "Invalid JSON"}), 400
    else:
        return redirect(url_for("auth.login"))

# Route that checks users's answers for the challenges


@ai_chat_bp.route("/check-answers", methods=["POST"])
def check_answers():
    if "user_id" in session:
        print(request.method)
        if request.method == "POST":
            data = request.get_json()
            user_code = data.get("user_code")
            
            if user_code:
                conn = sqlite3.connect("database/app.db")
                cursor = conn.cursor()

                challenge_id = session.get("challenge_id")
                user_id = session.get("user_id")

                cursor.execute("""
                                SELECT status
                                FROM Challenge_attempt
                                WHERE challenge_id=? AND
                                user_id=?""", (challenge_id, user_id,))

                status = cursor.fetchone()
                if status:
                    redirect_url = url_for(
                        "practice_hub.uncomplete_practice_challenges")
                    if status[0] == "Started":
                        cursor.execute("""
                                        SELECT question
                                    FROM Challenge WHERE challenge_id=?
                                """, (challenge_id,))

                        challenge = cursor.fetchone()[0]

                        language = session.get("language")
                        response = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"Given the code {user_code} and the challenge {challenge} from this programming language {language}, determine if the solution is correct. Reply only with Correct or Incorrect.",
                                },
                                {
                                    "role": "user",
                                    "content": f"code: {user_code}, challenge : {challenge} and programing language: {language}",
                                },
                            ],
                            temperature=1,
                            top_p=1,
                            model=model,
                        )

                        is_solution_correct = response.choices[0].message.content

                        print(is_solution_correct)

                        if is_solution_correct == "Correct":
                            completed_at = datetime.now().isoformat(timespec="seconds")

                            cursor.execute("""
                            UPDATE Challenge_attempt
                            SET completed_at = ?, status = ?
                            WHERE user_id = ? AND challenge_id = ?
                            """, (completed_at, "Completed", user_id, challenge_id))

                            conn.commit()
                            conn.close()
                            return jsonify({"redirect_url": redirect_url})
                        else:
                            return jsonify({"message": "Incorrect solution, Give another try!"})
                    elif status[0] == "Completed":
                        return jsonify({"redirect_url": url_for(
                        "practice_hub.uncomplete_practice_challenges")})
            else:
                return jsonify(
                    {"message": "You have to type the solution in the given code editor"})
    else:
        return redirect(url_for("auth.login"))
