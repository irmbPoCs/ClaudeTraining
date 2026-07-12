from dotenv import load_dotenv
from chat_helpers import *
from anthropic.types import MessageParam
import os

load_dotenv()

user_message : str = ""
chat_history :list[MessageParam] = []

print("Start chatting:")

chat_manager = ChatHelper(os.environ.get("ANTHROPIC_API_KEY"))

while user_message != 'quit!':
    user_message = input("(User)> ")
    chat_manager.add_user_message(message=user_message, chat_history= chat_history)
    response = chat_manager.send_conversation(chat_history=chat_history)
    chat_manager.add_assistant_message(message=response, chat_history=chat_history)
    chat_manager.print_last_message(chat_history=chat_history)