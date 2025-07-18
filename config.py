# config.py
import os
from dotenv import load_dotenv

# Load .env file only if not running on Railway
if os.environ.get("RAILWAY_ENVIRONMENT") is None:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Access all environment variables
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSKEY = os.getenv("GMAIL_PASSKEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SENDER_NAME = os.getenv("SENDER_NAME")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")
