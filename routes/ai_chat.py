"""
This module handles most of the AI parts in the application.
"""

import os
from datetime import datetime
from flask import Blueprint, session, url_for, request, jsonify
from openai import (OpenAI,
                    RateLimitError,
                    OpenAIError,
                    APIError,
                    AuthenticationError)
from dotenv import load_dotenv
from utils import login_required, db_execute, check_characters_limit

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=token,
)

ai_chat_bp = Blueprint("ai_chat", __name__)


def ai_response(system_content: str,
                user_input: str):
    """
    This is a function to generate the AI responses while handling errors

    made this function to reduce code repetition.

    Args:
        system_content (string): stores the role of the AI system
        user_input (string): stores the user input

    Returns:
        function returns a dictionary that has the error and the result.

    Raises:
        RateLimitError: If the request exceeds the allowed usage limits.
        AuthenticationError: If the provided API key is invalid or expired.
        APIError: If a generic OpenAI API error occurs.
        Exception: For any other unexpected errors.
    """
    error = ""
    result = ""

    result_or_error = {"error": error, "result": result}

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
    except APIError as e:
        error = f"OpenAI API error: {e}"
    except OpenAIError as e:
        error = f"generic openai api error: {e}"
    except Exception as e:
        error = f"An unexpected error occurred: {e}"

    result_or_error['error'] = error
    result_or_error['result'] = result
    return result_or_error


# AI Chat Route
@ai_chat_bp.route("/ai-chat", methods=["POST"])
@login_required
def chat():
    """
    This route gives the AI responses depending on the user's code,
    and the output that they got from their code

    This route has connected with the code_editor.html
    This route gets the user's typed code,
    the output they got after running the code,
    and the programming lnaguage that they are currently working on from
    the session variables,
    and the user's question from the frontend  (user_input).
    Then, call the ai_response function to retrieve the result,
    if the number of characters in user_input less than 1500.

    Returns:
        jsonified ai_response function's output with 200 code
    """
    language = session.get("language")
    user_code = session.get("user_code")
    code_output = session.get("output_of_code")

    data = request.get_json()
    user_input = data.get("user_input")

    # Limit to 1500 characters,
    # check the user input that is under 1500 characters,
    # before proceeding with the rest of the application.
    # This is due to the prevention of the crashing
    # Open API key and the backend
    if check_characters_limit(user_input, max_length=1500) == "max_reject":
        return jsonify({
            "warning":
            "Message too long. Please keep it under 1,500 characters."
        })

    # Checks whether the user input is empty
    if not user_input.strip():
        return jsonify({
            "warning": "Oops! Looks like you forgot to type your message."
        })

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
    """
    Handle AI course chat requests from the frontend.

    This route is connected to `ai-course.html`
    via `ai-course.js` (function: `ai_chat`).
    It receives `user_input` from the frontend, validates its length, and calls
    the `ai_response` function if the input is within the allowed limit.

    Args:
        None (input is received from the request JSON).

    Returns:
        Response (JSON):
            - If the input has fewer than 1500 characters,
              returns the JSONified
              output of `ai_response(user_input)`.
            - If the input exceeds 1500 characters, returns a JSONified error
              message:
              {
                  "error":
                  "Message too long. Please keep it under 1,500 characters."
              }

    """
    data = request.get_json()
    user_input = data.get("user_input")

    # Limit to 1500 characters,
    # check the user input that is under 1500 characters,
    # before proceeding with the rest of the application.
    # This is due to the prevention of the crashing
    # Open API key and the backend
    if check_characters_limit(user_input, max_length=1500) == "max_reject":
        return jsonify({
            "warning":
            "Message too long. Please keep it under 1,500 characters."})

    ai_course_topic = session.get("ai_course_topic")

    system_content = f"""You are an AI assistant built into
                        the Ada Learning Platform, created
                        by G. A. Pasindu Vidunitha.This platform helps users
                        learn new programming languages. Your role is to
                        assist learners by providing clear,
                        concise, and accurate explanations related
                        to {ai_course_topic}."""

    return jsonify(ai_response(system_content, user_input)), 200


# Route that checks users's answers for the challenges
@ai_chat_bp.route("/check-answers", methods=["POST"])
@login_required
def check_answers():
    """
    This route checks the user's answers for
    the challenges in the practice hub.
    This uses an OpenAI API key to check the answer.
    This route is connected to the challenge.html through the challenge.js.
    It gets the user's code (the user's answer) from the frontend.
    Checks that the user's code is less than 15,000 characters.
    First, it takes the `status` from the database,
    if the answer is correct, it changes to `Completed`.
    If the answer is wrong, it sends the message  "solution_wrong".

    Returns:
        - If the process is successful or if the status is completed,
        it sends the redirect_url to uncompleted challenges
        - If the answer is not correct, it sends solution_wrong
        - If the user has not typed anything, it sends the warning message
        - If the characters more than 15000, it sends a warning message
    """
    data = request.get_json()
    user_code = data.get("user_code")

    if check_characters_limit(user_code, max_length=15000) == "max_reject":
        return jsonify({
            "message": "Input too large (max 15,000 chars).",
            "message_type": "warning"
        })

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

        # Check if the status is not empty
        # Empty means user has not started
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

                solutions_query = """
                    SELECT Answer
                    FROM Solution
                    WHERE challenge_id = ? AND language = ?"""

                solutions = db_execute(query=solutions_query,
                                       fetch=True,
                                       fetchone=True,
                                       values=(session["challenge_id"],
                                               language))

                system_content = f"""Given {user_code} and {challenge}
                                    in {language}, decide if solution
                                    is correct. Reply only:
                                    Correct or Incorrect.
                                    Give priority to DB {solutions[0]}.
                                    If user code is similar and both solve it,
                                    reply Correct, else Incorrect.  """

                user_content = f"""code: {user_code},
                                    challenge : {challenge}
                                    and programing language: {language}"""
                
                print(system_content)

                is_solution_correct = ai_response(
                    system_content, user_content)

                if is_solution_correct['error']:
                    return jsonify({
                        "message": is_solution_correct["error"],
                        "message_type": "error"
                    })      

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
