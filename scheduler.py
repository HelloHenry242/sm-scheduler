from datetime import datetime
from models import SocialPost
from storage import Storage

# Explicitly import the validation layers from your team's regex file
import regex

class PostScheduler:
    def __init__(self, storage_instance: Storage = None):
        self.storage = storage_instance or Storage()

    def validate_inputs(self, title: str, caption: str, platform: str, date_str: str, time_str: str):
        """
        Validates user entries by delegating check operations to regex.py.
        """
        # 1. Presence / Empty checks
        if not regex.is_valid_title(title):
            raise ValueError("Title cannot be empty.")
        if not regex.is_valid_caption(caption):
            raise ValueError("Caption cannot be empty.")
        if not platform or not platform.strip():
            raise ValueError("Please select a platform.")

        # 2. Platform Compliance check
        if not regex.is_valid_platform(platform):
            raise ValueError(f"Platform '{platform}' is not supported by our system pipeline.")

        # 3. Date Format check via Regex
        if not regex.is_valid_date_format(date_str):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        # Real calendar bounds verification
        try:
            scheduled_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("The provided date is invalid (e.g., February 30th does not exist).")

        # 4. Time Format check via Regex
        if not regex.is_valid_time_format(time_str):
            raise ValueError("Invalid time format. Please use HH:MM (24-hour format).")

        # Real clock bounds verification
        try:
            scheduled_time = datetime.strptime(time_str.strip(), "%H:%M").time()
        except ValueError:
            raise ValueError("The provided time is invalid (Must be between 00:00 and 23:59).")

        return scheduled_date, scheduled_time

    def schedule_post(self, title: str, caption: str, platform: str, date_str: str, time_str: str, status: str = "Scheduled") -> SocialPost:
        """
        Validates parameters, creates the SocialPost asset object, and commits it to disk.
        """
        valid_date, valid_time = self.validate_inputs(title, caption, platform, date_str, time_str)

        new_post = SocialPost(
            title=title,
            caption=caption,
            platform=platform,
            scheduled_date=valid_date,
            scheduled_time=valid_time,
            status=status
        )

        self.storage.add_post(new_post)
        return new_post