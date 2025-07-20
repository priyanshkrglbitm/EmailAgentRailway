# twilio_utils.py
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, MY_WHATSAPP_NUMBER

# Use Twilio sandbox number unless you have a verified custom one
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # ✅ fixed sender

def send_whatsapp(message: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER
    )

