import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools import tool
from tools import send_email_with_attachment , read_latest_email


if os.environ.get("RAILWAY_ENVIRONMENT") is None:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Extract credentials from environment
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSKEY = os.getenv("GMAIL_PASSKEY")
api_key = os.getenv("GROQ_API_KEY")
SENDER_NAME = os.getenv("SENDER_NAME")


# Initialize LLM
llm = Groq(
    id="llama3-70b-8192",
    api_key=api_key
)

# Create the agent
email_agent = Agent(
    name="email_agent",
    role="Send emails via Gmail with the given details.",
    tools=[send_email_with_attachment , read_latest_email],
    model=llm,
    verbose=True
)

