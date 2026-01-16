from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# OpenAI setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        email_text = data.get("email") if data else None

        if not email_text:
            return jsonify({"reply": "No email content provided."})

        if not OPENAI_API_KEY:
            return jsonify({"reply": "OpenAI API key not found."})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional email assistant."
                },
                {
                    "role": "user",
                    "content": (
                        "Read the email and generate a polite, professional reply.\n\n"
                        f"Email:\n{email_text}"
                    )
                }
            ],
            temperature=0.4
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"reply": "Failed to generate reply from AI."})


if __name__ == "__main__":
    app.run(debug=True)
