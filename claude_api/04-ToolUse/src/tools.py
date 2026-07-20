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


def set_reminder(content, timestamp):
    print(f"-----\nSetting the following reminder for {timestamp}:\n{content}\n-----")


set_reminder_schema = ToolParam({
    "name": "set_reminder",
    "description": "Schedule a reminder to be delivered to the user at a specific date and time. Use this tool whenever the user asks to be reminded about something at a future moment (e.g., 'remind me to call the dentist tomorrow at 9am'). The tool stores the reminder text along with its scheduled time; it does not return any confirmation data or reminder ID, and it will not fire the reminder immediately. If the user's requested time is relative (e.g., 'in two hours'), resolve it to an absolute timestamp before calling this tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The reminder message to deliver to the user. Should be a concise, self-contained description of what the user wants to be reminded about (e.g., 'Call the dentist to reschedule appointment')."
            },
            "timestamp": {
                "type": "string",
                "description": "The absolute date and time at which the reminder should fire, in ISO 8601 format (e.g., '2026-07-20T09:00:00'). Must be a specific, non-relative timestamp; resolve any relative time expressions to an absolute value first."
            }
        },
        "required": ["content", "timestamp"]
    }
})

