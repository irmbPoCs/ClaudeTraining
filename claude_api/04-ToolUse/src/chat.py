from dotenv import load_dotenv
from chat_helpers import *
from tools import *
import os

load_dotenv()

user_message: str = ""

print("Start chatting:")

chat_setup = """
You are a general assistant for end users.

Guidelines:
* Date and times must use this format: "%Y-%m-%d %H:%M:%S". Unless the user explicitly request a different one.
"""
api_key = os.environ.get("ANTHROPIC_API_KEY")
max_tokens = int(os.environ.get("MAX_TOKENS"))
model = os.environ.get("MODEL")
temperature = float(os.environ.get("TEMPERATURE"))
function_tools = {
    "get_current_date": get_current_date,
    "add_days_to_datetime": add_days_to_datetime
}


chat_manager = ChatHelper(
    api_key=api_key,
    system_message=chat_setup,
    max_tokens=max_tokens,
    model=model,
    temperature=temperature,
    tools=[get_current_date_schema, add_days_to_datetime_schema],
    function_tools=function_tools
)

while user_message != 'quit!':
    user_message = input(f"{Colors.USER}(User)> {Colors.RESET}")
    chat_manager.add_user_message(message=user_message)
    chat_manager.process_conversation()
    # chat_manager.stream_conversation_2()
