from anthropic.types import ToolParam
from datetime import datetime


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_date_schema = ToolParam({
    "name": "get_current_date",
    "description": "Get the current date and time as a formatted string. Accepts an optional strftime-compatible format string; if omitted, defaults to '%Y-%m-%d %H:%M:%S' (e.g., '2026-07-18 14:30:00'). The format string must not be empty if provided.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A strftime-compatible format string used to format the current date and time (e.g., '%Y-%m-%d %H:%M:%S' for '2026-07-18 14:30:00', or '%B %d, %Y' for 'July 18, 2026'). Must not be empty."
            }
        },
        "required": []
    }
})

# print(get_current_date())
