import os
from datetime import datetime
from flask import Blueprint, session, url_for, request, jsonify
from openai import (OpenAI,
                    RateLimitError,
                    OpenAIError,
                    APIError,
                    AuthenticationError)
from dotenv import load_dotenv
from utils import login_required, db_execute

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=token,
)

ai_chat_bp = Blueprint("ai_chat", __name__)


def ai_response(system_content,
                user_input):
    result_or_error = {"error": "", "result": ""}
    error = ""
    result = ""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            temperature=1,
            top_p=1,
            model=MODEL,
        )
        result = response.choices[0].message.content
    except RateLimitError:
        error = "Rate limit exceed"
    except AuthenticationError:
        error = "Invalid or expired API key"
    except OpenAIError as e:
        error = f"generic openai api error: {e}"
    except APIError as e:
        error = f"OpenAI API error: {e}"
    except Exception as e:
        error = f"An unexpected error occurred: {e}"

    result_or_error['error'] = error
    result_or_error['result'] = result
    return result_or_error


# AI Chat Route
@ai_chat_bp.route("/ai-chat", methods=["POST"])
@login_required
def chat():
    language = session.get("language")
    user_code = session.get("user_code")
    data = request.get_json()
    user_input = data.get("user_input")
    code_output = session.get("output_of_code")

    system_content = f"""You are an AI assistant built
                        into the Ada Learning Platform,
                        created by G. A. Pasindu Vidunitha.
                        Your role is to help users
                        learn and understand {language} by
                        providing clear and concise
                        explanations. If they ask questions about
                        their written program—such
                        as {user_code} and the output
                        they received {code_output}—respond
                        with simple, direct answers
                        without unnecessary detail."""
    return jsonify(ai_response(system_content, user_input)), 200


@ai_chat_bp.route("/ai-course-chat", methods=["POST"])
@login_required
def ai_course_chat():
    data = request.get_json()
    user_input = data.get("user_input")
    ai_course_topic = session.get("ai_course_topic")
    system_content = f"""You are an AI assistant built into
                        the Ada Learning Platform, created
                        by G. A. Pasindu Vidunitha.This platform helps users
                        learn new programming languages. Your role is to
                        assist learners by providing clear,
                        concise, and accurate explanations related
                        to {ai_course_topic}."""
    ai_response(system_content, user_input)
    return jsonify(ai_response(system_content, user_input)), 200


# Route that checks users's answers for the challenges
@ai_chat_bp.route("/check-answers", methods=["POST"])
@login_required
def check_answers():
    data = request.get_json()
    user_code = data.get("user_code")

    if user_code:
        challenge_id = session.get("challenge_id")
        user_id = session.get("user_id")

        status_query = """
                        SELECT status
                        FROM Challenge_attempt
                        WHERE challenge_id=? AND
                        user_id=?"""

        status = db_execute(query=status_query,
                            fetch=True,
                            fetchone=True,
                            values=(challenge_id, user_id,))
        if status:
            redirect_url = url_for(
                "practice_hub.uncomplete_practice_challenges")
            if status[0] == "Started":
                question_query = """
                                SELECT question
                            FROM Challenge WHERE challenge_id=?
                        """

                challenge = db_execute(query=question_query,
                                       fetch=True,
                                       fetchone=True,
                                       values=(challenge_id,))[0]

                language = session.get("language")

                system_content = f"""Given the code {user_code}
                                    and the challenge {challenge} from this
                                    programming language {language},
                                    determine if the solution is correct.
                                    Reply only with Correct or Incorrect."""

                user_content = f"""code: {user_code},
                                    challenge : {challenge}
                                    and programing language: {language}"""

                is_solution_correct = ai_response(
                    system_content, user_content)

                if is_solution_correct['error']:
                    return jsonify({"error": is_solution_correct["error"]})

                if is_solution_correct["result"] == "Correct":
                    completed_at = datetime.now().isoformat(timespec="seconds")

                    update_query = """
                    UPDATE Challenge_attempt
                    SET completed_at = ?, status = ?
                    WHERE user_id = ? AND challenge_id = ?
                    """

                    db_execute(query=update_query,
                               values=(completed_at,
                                       "Completed",
                                       user_id,
                                       challenge_id))

                    return jsonify({"redirect_url": redirect_url})
                else:
                    return jsonify({"message_type": "solution_wrong"})
            elif status[0] == "Completed":
                return jsonify({"redirect_url": url_for(
                    "practice_hub.uncomplete_practice_challenges")})
    else:
        return jsonify({
            "message": ("You have to type the solution"
                        "in the given code editor"),
            "message_type": "warning"
        })
