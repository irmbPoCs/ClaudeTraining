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
    TOOL = "\033[90M"


class ChatHelper:

    def __init__(self, api_key, system_message: str = "", max_tokens=100, model="", temperature=0.0, tools=[], function_tools={}):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.system_message = None if system_message == "" else system_message
        self.chat_history: list[MessageParam] = []
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tools = tools
        self.function_tools = function_tools

    def add_user_message(self, message: str) -> None:
        self.add_message(message=message, role=USER_ROLE)

    def add_assistant_message(self, message: str) -> None:
        self.add_message(message=message, role=ASSISTANT_ROLE)

    def add_tool_use_message(self, tool_use_message) -> None:
        self.chat_history.append(
            {
                "role": "assistant",
                "content": [tool_use_message]
            })

    def add_tool_result_message(self, tool_use_message_content, tool_result) -> None:
        self.chat_history.append(
            {
                "role": "user",
                "content": [
                    {
                        "tool_use_id": tool_use_message_content.id,
                        "type": "tool_result",
                        "content": f"{tool_result}",
                        "is_error": False
                    }
                ]
            }
        )

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
            temperature=self.temperature,
            tools=self.tools
        )

        return response

    def process_conversation(self):

        response = self.send_conversation()
        response_content = response.content[0]

        if response_content.type == "tool_use":
            self.print_message(
                "TOOL", f"Calling tool: {response_content.name}", Colors.TOOL)
            self.add_tool_use_message(response_content)
            selected_tool = self.function_tools[response_content.name]
            tool_result = selected_tool(**response_content.input)
            self.add_tool_result_message(response_content, tool_result)
            self.print_message(
                "TOOL", f"Tool result: {tool_result}", Colors.TOOL)
            return self.process_conversation()
        elif response_content.type == "text":
            assistant_message = response_content.text
            self.add_assistant_message(assistant_message)
            self.print_message(
                ASSISTANT_ROLE, assistant_message, Colors.ASSISTANT)
            return assistant_message

    def stream_conversation_1(self):

        stream = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.chat_history,
            system=self.system_message,
            temperature=self.temperature,
            stream=True,
            tools=self.tools
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
            stream=True,
            tools=self.tools
        ) as stream:

            message = ""
            for stream_part in stream:
                if hasattr(stream_part, 'delta') and hasattr(stream_part.delta, 'text'):
                    text = stream_part.delta.text
                    message += text
                    self.print_message(ASSISTANT_ROLE, text, Colors.ASSISTANT)

            self.add_assistant_message(message)
