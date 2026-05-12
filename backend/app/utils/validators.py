# validators.py — input validation helpers
import re


def validate_phone(contact: str) -> bool:
    """Basic Pakistan phone number validation."""
    # Accepts formats like 03001234567, +923001234567
    pattern = r"^(\+92|0)[0-9]{10}$"
    return bool(re.match(pattern, contact.replace(" ", "").replace("-", "")))


def validate_date(date_str: str) -> bool:
    """Validate date string YYYY-MM-DD."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_str))


def validate_time(time_str: str) -> bool:
    """Validate time string HH:MM."""
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, time_str))
