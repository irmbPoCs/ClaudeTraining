from anthropic import Anthropic
from anthropic.types import MessageParam, Message

client = Anthropic()

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"
SYSTEM_ROLE = "system"


class Colors:
    USER = "\033[94m"  # Blue
    ASSISTANT = "\033[92m"  # Green
    RESET = "\033[0m"  # Reset to default
    TOOL = "\033[90m" # Bright black


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

    def add_user_message(self, message) -> None:
        self.add_message(message=message, role=USER_ROLE)

    def add_assistant_message(self, message) -> None:
        self.add_message(message=message, role=ASSISTANT_ROLE)

    def add_tool_use_message(self, message) -> None:
        content = message.content if isinstance(message, Message) else message
        self.chat_history.append({"role": "assistant", "content": content})


    def add_tool_result_message(self, tool_results: list) -> None:
        self.chat_history.append({"role": "user", "content": tool_results})

    def add_message(self, message, role: str) -> None:
        self.chat_history.append(
            {
                "role": role,
                "content": message.content if isinstance(message, Message) else message
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

    def execute_tool(self, tool_use) -> dict:
        self.print_message("TOOL", f"Calling tool: {tool_use.name}", Colors.TOOL)
        try:
            selected_tool = self.function_tools[tool_use.name]
            tool_result = selected_tool(**tool_use.input)
            self.print_message("TOOL", f"Tool result: {tool_result}", Colors.TOOL)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"{tool_result}",
                "is_error": False,
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"Error: {e}",
                "is_error": True,
            }

    def process_conversation(self):

        response = self.send_conversation()

        # Keep resolving tool calls until Claude returns a final text turn.
        # "tool_use"  -> client tools (function_tools) we execute locally.
        # "pause_turn" -> a server tool (e.g. web_search) hit its iteration
        #                 limit; re-send the paused turn so the server resumes.
        while response.stop_reason in ("tool_use", "pause_turn"):
            self.add_tool_use_message(response)
            tool_results = [
                self.execute_tool(block)
                for block in response.content
                if block.type == "tool_use"
            ]
            # Only client tool_use blocks produce results. A pure server-tool
            # pause has none — don't append an empty (invalid) user message.
            if tool_results:
                self.add_tool_result_message(tool_results)
            response = self.send_conversation()

        assistant_message = "".join(
            block.text for block in response.content if block.type == "text"
        )

        # Surface web search sources (citations live on the final text blocks).
        sources = self.extract_web_search_citations(response)
        if sources:
            listed = "\n".join(
                f"  [{i}] {title} — {url}"
                for i, (url, title) in enumerate(sources, start=1)
            )
            assistant_message = f"{assistant_message}\n\nSources:\n{listed}"

        self.add_assistant_message(assistant_message)
        self.print_message(ASSISTANT_ROLE, assistant_message, Colors.ASSISTANT)
        return assistant_message

    def extract_web_search_citations(self, response) -> list[tuple]:
        """Collect unique (url, title) pairs cited from web search results."""
        seen: set[str] = set()
        sources: list[tuple] = []
        for block in response.content:
            if block.type != "text":
                continue
            for citation in getattr(block, "citations", None) or []:
                if getattr(citation, "type", None) != "web_search_result_location":
                    continue
                url = getattr(citation, "url", None)
                if url and url not in seen:
                    seen.add(url)
                    sources.append((url, getattr(citation, "title", None) or url))
        return sources

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
