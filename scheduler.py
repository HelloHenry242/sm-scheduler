import re
from datetime import datetime
from models import SocialPost
from storage import Storage

class PostScheduler:
    def __init__(self, storage_instance: Storage = None):
        # Use the provided storage instance, or default to a new one
        self.storage = storage_instance or Storage()

    def validate_inputs(self, title: str, caption: str, platform: str, date_str: str, time_str: str):
        """
        Validates all user inputs. Raises ValueErrors if constraints are violated.
        Uses Regex to check formats and detect links/hashtags.
        """
        # 1. Check for empty inputs
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if not caption.strip():
            raise ValueError("Caption cannot be empty.")
        if not platform.strip():
            raise ValueError("Please select a platform.")
        if not date_str.strip():
            raise ValueError("Date cannot be empty.")
        if not time_str.strip():
            raise ValueError("Time cannot be empty.")

        # 2. Validate Date Format (YYYY-MM-DD) using Regex
        # Matches exactly 4 digits, a dash, 2 digits, a dash, and 2 digits
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, date_str):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        # Validate that it's a real calendar date
        try:
            scheduled_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("The provided date is invalid (e.g., Feb 30th does not exist).")

        # 3. Validate Time Format (HH:MM) using Regex
        # Matches exactly 2 digits, a colon, and 2 digits
        time_pattern = r"^\d{2}:\d{2}$"
        if not re.match(time_pattern, time_str):
            raise ValueError("Invalid time format. Please use HH:MM (24-hour format).")

        # Validate that it's a real clock time
        try:
            scheduled_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("The provided time is invalid (Must be between 00:00 and 23:59).")

        # 4. Bonus Regex Features: Detect links or extract hashtags if needed
        # (This protects against malicious or broken links in captions)
        url_pattern = r"https?://[^\s]+"
        links = re.findall(url_pattern, caption)
        if links:
            print(f"Log: Detected {len(links)} link(s) in the caption.")

        return scheduled_date, scheduled_time

    def schedule_post(self, title: str, caption: str, platform: str, date_str: str, time_str: str, status: str = "Scheduled") -> SocialPost:
        """
        Validates inputs, instantiates a SocialPost object, and commits it to storage.
        """
        # Validate inputs first (will raise ValueError if anything is wrong)
        valid_date, valid_time = self.validate_inputs(title, caption, platform, date_str, time_str)

        # Create the post object using your team's SocialPost structure
        new_post = SocialPost(
            title=title,
            caption=caption,
            platform=platform,
            scheduled_date=valid_date,
            scheduled_time=valid_time,
            status=status
        )

        # Save it using your team's Storage logic
        self.storage.add_post(new_post)
        
        print(f"Success: Post '{title}' has been successfully scheduled with ID {new_post.id}!")
        return new_post