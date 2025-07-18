# twilio_utils.py
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, MY_WHATSAPP_NUMBER

def send_whatsapp(message: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER
    )
