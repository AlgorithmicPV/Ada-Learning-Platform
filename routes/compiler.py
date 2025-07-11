from flask import Blueprint, session, redirect, url_for, request, jsonify
from pistonpy import PistonApp

piston = PistonApp()

compiler_bp = Blueprint("compiler", __name__)

# Route that get the language from the challenge page
@compiler_bp.route("/get-language", methods=["POST"])
def get_the_language():
    if "user_id" in session:
        if request.is_json and request.method == "POST":
            data = request.get_json()
            session["language"] = data.get("language")
        return "",204
    else:
        return redirect(url_for("auth.login"))


# Compiler Route
@compiler_bp.route("/compiler", methods=["POST"])
def compiler():
    if "user_id" in session:
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
    else:
        return redirect(url_for("auth.login"))

