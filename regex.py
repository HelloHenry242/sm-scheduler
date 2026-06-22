import re

def is_valid_title(title):
    return title.strip() != ""

def is_valid_caption(caption):
    return caption.strip() != ""

def is_valid_date(date):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, date) is not None

def is_valid_time(time):
    pattern = r"^\d{2}:\d{2}$"
    return re.match(pattern, time) is not None

def is_valid_platform(platform):
    platforms = ["LinkedIn", "Twitter", "Instagram", "Facebook"]
    return platform in platforms

if __name__ == "__main__":
    print(is_valid_title("My Post"))       # True
    print(is_valid_title(""))              # False
    print(is_valid_caption("Hello!"))      # True
    print(is_valid_caption(""))            # False
    print(is_valid_date("2026-06-20"))     # True
    print(is_valid_date("hello"))          # False
    print(is_valid_time("14:30"))          # True
    print(is_valid_time("9am"))            # False
    print(is_valid_platform("LinkedIn"))   # True
    print(is_valid_platform("MySpace"))    # False