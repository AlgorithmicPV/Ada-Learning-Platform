"""
Handles the Code compiling for the application
"""

from flask import Blueprint, session, request, jsonify
from pistonpy import PistonApp
from utils import login_required, check_characters_limit

piston = PistonApp()

compiler_bp = Blueprint("compiler", __name__)


# Route that get the language from the challenge page
@compiler_bp.route("/get-language", methods=["POST"])
@login_required
def get_the_language():
    """
    This route saves the selected language from the challenge page.

    The function reads JSON data from the POST request, gets the chosen
    language, and stores it in the session. It then returns an empty
    response with a 200 status code.


    Returns:
        Response: Empty string with status code 200.
    """
    data = request.get_json()
    session["language"] = data.get("language")
    return "", 200


# Compiler Route
@compiler_bp.route("/compiler", methods=["POST"])
@login_required
def compiler():
    """
    This route compiles and runs the user's code in the selected language.

    The function checks that the request is JSON and reads the user's code
    and input. It validates the code length (max 15,000 characters). If it
    is valid, it runs the code using Piston with the chosen language and
    returns the output in JSON. The user's code and output are also stored
    in the session. If the request is invalid, it returns an error with a
    400 status.

    Args:
        None (values are taken from the request body and session).

    Returns:
        Response: JSON object with the program output, or an error message.
    """
    if request.is_json and request.method == "POST":
        language = session.get("language").lower()
        data = request.get_json()
        user_code = data.get("user_code")

        if check_characters_limit(user_code, max_length=15000) == "max_reject":
            return jsonify({"warning": "Input too large (max 15,000 chars)."})

        session["user_code"] = user_code
        user_input = data.get("user_input")
        output = piston.run(
            language=language,
            code=user_code,
            input=user_input,
        )
        session["output_of_code"] = {"output": output["run"]["output"]}
        return jsonify({"output": output["run"]["output"]}), 200
    else:
        return jsonify({"error": "Invalid JSON"}), 400
