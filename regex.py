import re

def is_valid_title(title: str) -> bool:
    return bool(title and title.strip())

def is_valid_caption(caption: str) -> bool:
    return bool(caption and caption.strip())

def is_valid_date_format(date_str: str) -> bool:
    # Checks for exactly YYYY-MM-DD
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_str.strip()))

def is_valid_time_format(time_str: str) -> bool:
    # Checks for exactly HH:MM (24-hour)
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, time_str.strip()))

def is_valid_platform(platform: str) -> bool:
    valid_platforms = ["LinkedIn", "Instagram", "Twitter/X", "Facebook"]
    return platform.strip() in valid_platforms

def detect_links(text: str) -> list:
    url_pattern = r"(https?://\S+|www\.\S+)"
    return re.findall(url_pattern, text)

def validate_hashtags(text: str) -> list:
    hashtag_pattern = r"#\w+"
    return re.findall(hashtag_pattern, text)