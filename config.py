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

# ✅ Optional: Debug print — ONLY enable locally
if os.environ.get("RAILWAY_ENVIRONMENT") is None:
    print(f"[LOCAL DEBUG] GMAIL_EMAIL: {GMAIL_EMAIL}, TWILIO_SID: {TWILIO_ACCOUNT_SID}")

# ✅ Validation — fail fast if any critical env var is missing
required_vars = {
    "GMAIL_EMAIL": GMAIL_EMAIL,
    "GMAIL_PASSKEY": GMAIL_PASSKEY,
    "GROQ_API_KEY": GROQ_API_KEY,
    "SENDER_NAME": SENDER_NAME,
    "TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
    "TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
    "TWILIO_WHATSAPP_NUMBER": TWILIO_WHATSAPP_NUMBER,
    "MY_WHATSAPP_NUMBER": MY_WHATSAPP_NUMBER,
}

missing = [key for key, val in required_vars.items() if not val]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
