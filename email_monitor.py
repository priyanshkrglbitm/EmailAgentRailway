import schedule, time, json
from tools import read_latest_email_logic
from twilio_utils import send_whatsapp
import os



last_seen_subject = None

def check_new_email():
    global last_seen_subject
    result = json.loads(read_latest_email_logic())

    if "error" in result:
        print("❌ Email read error:", result["error"])
        return

    subject = result.get("Subject")
    sender = result.get("From")
    summary = result.get("Summary")

    if subject != last_seen_subject:
        msg = f"📩 New Email from {sender}\nSubject: {subject}\n\n{summary}"
        send_whatsapp(msg)
        last_seen_subject = subject
        print("✅ Summary sent.")
    else:
        print("📭 No new email.")

if __name__ == "__main__":
    print("📡 Email monitoring started...")
    schedule.every(2).minutes.do(check_new_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

