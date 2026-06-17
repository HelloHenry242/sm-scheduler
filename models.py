import uuid

class SocialPost:
    """
    This class serves as the structure for our sm-posts , holding the info we need from each user.
    """
    def __init__(self, title, caption, platform, scheduled_date, scheduled_time, status="Draft"):
        # We give every post an ID so we don't mix them up when saving/loading
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.caption = caption
        self.platform = platform
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        self.status = status

    def to_dict(self):
        """
        This method converts our sm-post to a dictionary because json files cannot read python objects.
        """
        return {
            "id": self.id,
            "title": self.title,
            "caption": self.caption,
            "platform": self.platform,
            "date": str(self.scheduled_date),
            "time": str(self.scheduled_time),
            "status": self.status
        }

def post_from_dict(data):
    """
    Reverse the process: turn the stored JSON data back into a usable object.
    We use .get() to avoid crashing if a field happens to be missing.
    """
    return SocialPost(
        title=data.get('title'),
        caption=data.get('caption'),
        platform=data.get('platform'),
        scheduled_date=data.get('date'),
        scheduled_time=data.get('time'),
        status=data.get('status', 'Draft') # Default to Draft if nothing else is specified
    )