from anthropic.types import ToolParam
from datetime import datetime, timedelta


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


def add_days_to_datetime(date_time: datetime | str, duration_in_days: int):
    if isinstance(date_time, str):
        date_time = datetime.fromisoformat(date_time)
    return date_time + timedelta(days=duration_in_days)


add_days_to_datetime_schema = ToolParam({
    "name": "add_days_to_datetime",
    "description": "Add a specified number of days to a datetime object and return the new datetime.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_time": {
                "type": "string",
                "description": "The datetime to which days will be added (ISO 8601 format, e.g., '2024-01-15T10:30:00')"
            },
            "duration_in_days": {
                "type": "integer",
                "description": "The number of days to add to the datetime. Use negative values to subtract days."
            }
        },
        "required": ["date_time", "duration_in_days"]
    }
})
