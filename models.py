import uuid

class SocialPost:
    def __init__(self, title, caption, platform, scheduled_date, scheduled_time, status="Draft", id=None):
        # Allow passing an existing ID when loading from file, otherwise generate new
        self.id = id if id else str(uuid.uuid4())[:8]
        self.title = title
        self.caption = caption
        self.platform = platform
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        self.status = status

    def to_dict(self):
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
    return SocialPost(
        id=data.get('id'),
        title=data.get('title'),
        caption=data.get('caption'),
        platform=data.get('platform'),
        scheduled_date=data.get('date'),
        scheduled_time=data.get('time'),
        status=data.get('status', 'Draft')
    )