from flask import Flask, request, Response
from EmailAgent import email_agent
from twilio_utils import send_whatsapp
import os 

app = Flask(__name__)
user_state = {}


@app.route("/")
def index():
    return "✅ Email Agent is running."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.form.get("Body").strip().lower()
    sender = request.form.get("From")

    state = user_state.get(sender, {})
    reply = ""

    if incoming_msg == "hi" or incoming_msg=="Hi":
        user_state[sender] = {"step": "email_to"}
        reply = "👋 Hello Priyanshu! Who should I email?"
    elif state.get("step") == "email_to":
        user_state[sender]["to"] = incoming_msg
        user_state[sender]["step"] = "email_subject"
        reply = "📌 Got it. What is the subject?"
    elif state.get("step") == "email_subject":
        user_state[sender]["subject"] = incoming_msg
        user_state[sender]["step"] = "email_body"
        reply = "📝 Please provide a brief body for the email."
    elif state.get("step") == "email_body":
        prompt = (
            f"Use Gmail to send an email to '{user_state[sender]['to']}' "
            f"with subject '{user_state[sender]['subject']}'. "
            f"Generate a professional body from this summary: '{incoming_msg}' "
            f"and sign as '{os.getenv('SENDER_NAME')}'."
        )
        result = email_agent.run(message=prompt)
        reply = "✅ Email sent successfully!"
        user_state.pop(sender)
    else:
        reply = "👋 Send 'Hi' to start composing an email."

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

if __name__ == "__main__":
    app.run(port=5000)



