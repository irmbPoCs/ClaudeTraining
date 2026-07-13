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

chat_manager = ChatHelper(os.environ.get(
    "ANTHROPIC_API_KEY"), system_message=chat_setup)

while user_message != 'quit!':
    user_message = input(f"{Colors.USER}(User)> {Colors.RESET}")
    chat_manager.add_user_message(message=user_message)
    chat_manager.send_conversation()
    # chat_manager.add_assistant_message(message=response)    #chat_manager.print_last_message()
