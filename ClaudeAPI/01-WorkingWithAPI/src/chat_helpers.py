from anthropic import Anthropic
from anthropic.types import MessageParam

model = "claude-haiku-4-5"
MAX_TOKENS = 1000

client = Anthropic()

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"
SYSTEM_ROLE = "system"


class Colors:
    USER = "\033[94m"  # Blue
    ASSISTANT = "\033[92m"  # Green
    RESET = "\033[0m"  # Reset to default


class ChatHelper:

    def __init__(self, api_key, system_message: str = ""):
        self.client = Anthropic(api_key=api_key)
        self.system_message = None if system_message == "" else system_message
        self.chat_history: list[MessageParam] = []
        

    def add_user_message(self, message: str) -> None:
        self.add_message(message=message, role=USER_ROLE)

    def add_assistant_message(self, message: str) -> None:
        self.add_message(message=message, role=ASSISTANT_ROLE)

    def add_message(self, message: str, role: str) -> None:
        self.chat_history.append(
            {
                "role": role,
                "content": message
            }
        )

    def print_message(self, user_role, message, color):
        print(f"{color}({user_role})> {message}{Colors.RESET}")

    def send_conversation(self):

        response = self.client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=self.chat_history,
            system=self.system_message
        )

        assistant_message = response.content[0].text
        self.add_assistant_message(assistant_message)
        self.print_message(ASSISTANT_ROLE, assistant_message, Colors.ASSISTANT)
        return assistant_message
