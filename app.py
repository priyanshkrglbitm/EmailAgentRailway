from flask import Flask, request
from twilio_utils import download_media
from tools import send_email_with_attachment  # No longer used directly
import os

app = Flask(__name__)
user_state = {}

# Assume email_agent_with_attachment is imported and has a .run(message=..., attachment_path=None)
from your_agent_module import email_agent_with_attachment

@app.route("/")
def index():
    return "✅ Email Agent is running."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From")
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    state = user_state.get(sender, {})
    reply = ""

    if incoming_msg.lower() == "hi":
        user_state[sender] = {"step": "email_to"}
        reply = "👋 Hello Priyanshu! Who should I email?"

    elif state.get("step") == "email_to":
        state["to"] = incoming_msg
        state["step"] = "email_subject"
        reply = "📌 Got it. What is the subject?"

    elif state.get("step") == "email_subject":
        state["subject"] = incoming_msg
        state["step"] = "email_body"
        reply = "📝 Please provide a brief body for the email."

    elif state.get("step") == "email_body":
        state["body"] = incoming_msg
        state["step"] = "attach_prompt"
        reply = "📎 Do you want to attach a file? (yes/no)"

    elif state.get("step") == "attach_prompt":
        if incoming_msg.lower() == "yes":
            state["step"] = "awaiting_file"
            reply = "📤 Please upload your file now (PDF, DOCX, etc)."
        else:
            # When NOT attaching file, call with prompt only
            prompt = (
                f"Use Gmail to send an email to '{state['to']}' "
                f"with subject '{state['subject']}'. "
                f"Generate a professional body from this summary: '{state['body']}' "
                f"and sign as '{os.getenv('SENDER_NAME')}'."
            )
            result = email_agent_with_attachment.run(message=prompt, attachment_path=None)
            reply = "✅ Email sent successfully!"
            user_state.pop(sender)
    
    elif state.get("step") == "awaiting_file" and media_url:
        filename = f"/tmp/{sender.replace(':', '_')}_attachment"
        path = download_media(media_url, filename)
        # When attaching file, call with prompt and path
        prompt = (
            f"Use Gmail to send an email to '{state['to']}' "
            f"with subject '{state['subject']}'. "
            f"Generate a professional body from this summary: '{state['body']}' "
            f"and sign as '{os.getenv('SENDER_NAME')}'."
        )
        result = email_agent_with_attachment.run(message=prompt, attachment_path=path)
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
