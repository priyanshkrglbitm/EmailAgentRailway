from flask import Flask, request, Response
from EmailAgent import email_agent
import os 

app = Flask(__name__)
user_state = {}


@app.route("/")
def index():
    return "✅ Email Agent is running."

