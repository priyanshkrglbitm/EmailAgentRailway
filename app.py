from flask import Flask, request
from twilio_utils import download_media
import os
from EmailAgent import email_agent 

app = Flask(__name__)
user_state = {}

@app.route("/")
def index():
    return "✅ Email Agent is running."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming = request.form.get("Body", "").strip()
    sender = request.form.get("From")
    media_url = request.form.get("MediaUrl0")

    state = user_state.get(sender, {})
    reply = "👋 Send 'Hi' to start composing an email."

    if incoming.lower() == "hi":
        state = {"step": "email_to"}
        reply = "👋 Hello! Who should I email?"
    elif state.get("step") == "email_to":
        state["to"] = incoming
        state["step"] = "email_subject"
        reply = "📌 Got it. Subject?"
    elif state.get("step") == "email_subject":
        state["subject"] = incoming
        state["step"] = "email_body"
        reply = "📝 Now, write a short summary for the email."
    elif state.get("step") == "email_body":
        state["body"] = incoming
        state["step"] = "attach_prompt"
        reply = "📎 Attach a file? (yes/no)"
    elif state.get("step") == "attach_prompt":
        if incoming.lower() == "yes":
            state["step"] = "awaiting_file"
            reply = "📤 Please upload your file now."
        else:
            prompt = (
                f"Use Gmail to send an email to '{state['to']}' "
                f"with subject '{state['subject']}'. "
                f"Generate a proper body from this summary: '{state['body']}' "
                f"and sign as '{os.getenv('SENDER_NAME')}'."
            )
            email_agent.run(message=prompt, attachment_path=None)
            user_state.pop(sender, None)
            reply = "✅ Email sent without attachment!"
    elif state.get("step") == "awaiting_file" and media_url:
        path = download_media(media_url, f"/tmp/{sender.replace(':','_')}_attach")
        prompt = (
            f"Use Gmail to send an email to '{state['to']}' "
            f"with subject '{state['subject']}'. "
            f"Generate a proper body from this summary: '{state['body']}' "
            f"and sign as '{os.getenv('SENDER_NAME')}'."
        )
        email_agent.run(message=prompt, attachment_path=path)
        user_state.pop(sender, None)
        reply = "✅ Email sent with attachment!"
    else:
        pass

    user_state[sender] = state
    return f"""<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply}</Message></Response>"""

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
