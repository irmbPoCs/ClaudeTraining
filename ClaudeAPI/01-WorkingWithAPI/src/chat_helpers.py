from anthropic import Anthropic
from anthropic.types import MessageParam

model = "claude-haiku-4-5"
MAX_TOKENS = 1000

client = Anthropic()

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"


class ChatHelper:

    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def add_user_message(self, message: str, chat_history: list[MessageParam]) -> None:
        self.add_message(message=message, role=USER_ROLE,
                         chat_history=chat_history)

    def add_assistant_message(self, message: str, chat_history: list[MessageParam]) -> None:
        self.add_message(message=message, role=ASSISTANT_ROLE,
                         chat_history=chat_history)

    def add_message(self, message: str, role: str, chat_history: list[MessageParam]) -> None:
        chat_history.append(
            {
                "role": role,
                "content": message
            }
        )

    def print_last_message(self, chat_history: list[MessageParam]):
        last_message = chat_history[-1]
        print(f"(Assistant)> {last_message["content"]}")

    def send_conversation(self, chat_history: list[MessageParam]):
        response = self.client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=chat_history
        )
        return response.content[0].text
