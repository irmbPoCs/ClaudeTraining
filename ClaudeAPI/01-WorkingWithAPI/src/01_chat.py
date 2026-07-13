from dotenv import load_dotenv
from chat_helpers import *
import os

load_dotenv()

user_message: str = ""

print("Start chatting:")

chat_setup = """
You are an assistan for research and recommend the best practices about software development

Your recommendations must consider:
* SOLID Principles
* Design Patterns
* Focus on Enterprise Software

IMPORTANT:
* Do not provide information about different topics than software development
"""
api_key = os.environ.get("ANTHROPIC_API_KEY")
max_tokens = int(os.environ.get("MAX_TOKENS"))
model = os.environ.get("MODEL")
temperature = float(os.environ.get("TEMPERATURE"))

chat_manager = ChatHelper(
    api_key=api_key,
    system_message=chat_setup,
    max_tokens=max_tokens,
    model=model,
    temperature = temperature
)

while user_message != 'quit!':
    user_message = input(f"{Colors.USER}(User)> {Colors.RESET}")
    chat_manager.add_user_message(message=user_message)
    chat_manager.send_conversation()
