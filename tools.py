from phi.tools import tool
import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
import json

from config import GMAIL_EMAIL, GMAIL_PASSKEY

# --- Tool: Send Email ---
@tool
def send_email(to: str, subject: str, body: str) -> str:
    msg = MIMEText(body)
    msg["From"] = GMAIL_EMAIL
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_EMAIL, GMAIL_PASSKEY)
        smtp.send_message(msg)

    return f"Email sent to {to} with subject '{subject}'."

# --- Core Email Reader Logic ---
def read_latest_email_logic(
    email_user: str = GMAIL_EMAIL,
    email_pass: str = GMAIL_PASSKEY
) -> str:
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")

        status, data = mail.search(None, "ALL")
        email_ids = data[0].split()
        if not email_ids:
            return json.dumps({"error": "No emails found"})

        latest_email_id = email_ids[-1]
        status, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        from_ = msg["From"]

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    charset = part.get_content_charset() or "utf-8"
                    body = part.get_payload(decode=True).decode(charset, errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        summary = {
            "From": from_,
            "Subject": subject,
            "Summary": body.strip()[:300] + "..." if len(body) > 300 else body.strip()
        }

        return json.dumps(summary)

    except Exception as e:
        return json.dumps({"error": str(e)})

# --- Tool Wrapper for Agent ---
@tool()
def read_latest_email(email_user: str, email_pass: str) -> str:
    """
    Tool for agent: Reads the latest email and returns From, Subject, and Summary.
    """
    return read_latest_email_logic(email_user, email_pass)
