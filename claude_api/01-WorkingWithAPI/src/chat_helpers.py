from anthropic import Anthropic
from anthropic.types import MessageParam

client = Anthropic()

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"
SYSTEM_ROLE = "system"


class Colors:
    USER = "\033[94m"  # Blue
    ASSISTANT = "\033[92m"  # Green
    RESET = "\033[0m"  # Reset to default


class ChatHelper:

    def __init__(self, api_key, system_message: str = "", max_tokens=100, model="", temperature=0.0):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.system_message = None if system_message == "" else system_message
        self.chat_history: list[MessageParam] = []
        self.max_tokens = max_tokens
        self.temperature = temperature

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
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.chat_history,
            system=self.system_message,
            temperature=self.temperature
        )

        assistant_message = response.content[0].text
        self.add_assistant_message(assistant_message)
        self.print_message(ASSISTANT_ROLE, assistant_message, Colors.ASSISTANT)
        return assistant_message

    def stream_conversation_1(self):

        stream = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.chat_history,
            system=self.system_message,
            temperature=self.temperature,
            stream=True
        )

        response = ""
        for stream_part in stream:
            if hasattr(stream_part, 'delta') and hasattr(stream_part.delta, 'text'):
                text = stream_part.delta.text
                response += text
                self.print_message(ASSISTANT_ROLE, text, Colors.ASSISTANT)

        self.add_assistant_message(response)

    def stream_conversation_2(self):

        with self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.chat_history,
            system=self.system_message,
            temperature=self.temperature,
            stream=True
        ) as stream:

            for stream_part in stream:
                if hasattr(stream_part, 'delta') and hasattr(stream_part.delta, 'text'):
                    text = stream_part.delta.text
                    self.print_message(ASSISTANT_ROLE, text, Colors.ASSISTANT)

            self.add_assistant_message(stream.get_final_message())
