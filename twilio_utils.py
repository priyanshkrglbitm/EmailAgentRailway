from twilio.rest import Client
import os

def send_whatsapp(message: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=os.getenv("MY_WHATSAPP_NUMBER")
    )
