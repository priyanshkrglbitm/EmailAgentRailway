import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools import tool
from tools import send_email , read_latest_email


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
    tools=[send_email , read_latest_email],
    model=llm,
    verbose=True
)

# # Entrypoint
# if __name__ == "__main__":
#     print("--- Email Agent ---\n")

#     print("What would you like to do?")
#     print("1. Send an Email")
#     print("2. Read the Latest Gmail Email")
#     choice = input("Enter your choice (1 or 2): ").strip()

#     if choice == "1":
#         receiver_email = input("Receiver Email Address: ").strip()
#         subject = input("Enter Subject of your Mail: ").strip()
#         brief_summary = input("Describe briefly what this email is about: ").strip()

#         message_prompt = (
#             f"Use Gmail to send an email to '{receiver_email}' with subject '{subject}'. "
#             f"Generate a formal and professional email body based on this summary: '{brief_summary}', "
#             f"and sign it at the end with '{SENDER_NAME}'."
#         )

#         result = email_agent.run(message=message_prompt)
#         print(result)

#     elif choice == "2":
#         message_prompt = (
#             f"Use Gmail credentials to read the latest email and summarize its subject, sender, and body."
#         )
#         result = email_agent.run(message=message_prompt)
#         print(result)

#     else:
#         print("Invalid choice. Please select 1 or 2.")
