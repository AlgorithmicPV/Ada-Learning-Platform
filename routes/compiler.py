from flask import Blueprint, session, request, jsonify
from pistonpy import PistonApp
from utils import login_required

piston = PistonApp()

compiler_bp = Blueprint("compiler", __name__)


# Route that get the language from the challenge page
@compiler_bp.route("/get-language", methods=["POST"])
@login_required
def get_the_language():
    data = request.get_json()
    session["language"] = data.get("language")
    return "", 200


# Compiler Route
@compiler_bp.route("/compiler", methods=["POST"])
@login_required
def compiler():
    if request.is_json and request.method == "POST":
        language = session.get("language").lower()
        data = request.get_json()
        user_Code = data.get("user_code")
        session["user_code"] = user_Code
        user_input = data.get("user_input")
        output = piston.run(
            language=language,
            code=user_Code,
            input=user_input,
        )
        session["output_of_code"] = {"output": output["run"]["output"]}
        return jsonify({"output": output["run"]["output"]}), 200
    else:
        return jsonify({"error": "Invalid JSON"}), 400
