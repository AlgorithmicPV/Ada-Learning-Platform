from flask import Blueprint, session, redirect, url_for, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv


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
