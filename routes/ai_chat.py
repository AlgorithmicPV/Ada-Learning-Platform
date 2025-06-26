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
            data = request.get_json()
            user_input = data.get("user_input")
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI assistant integrated into Ada Learning Platform developed by G. A. Pasindu Vidunitha, designed to help users learn and understand {language} by providing clear explanations, guidance, and answers to their programming questions.",
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
            return jsonify({"response": response.choices[0].message.content}), 200
        else:
            return jsonify({"error": "Invalid JSON"}), 400
    else:
        return redirect(url_for("auth.login"))
