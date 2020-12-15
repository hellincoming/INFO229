from slack import WebClient
from nestorbot import NestorBot
import os

# Create a slack client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get a new NestorBot
nestor_bot = NestorBot("#bot")

# Get the onboarding message payload
message = nestor_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)
