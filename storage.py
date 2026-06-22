import json
import os
from models import SocialPost, post_from_dict

class Storage:
    def __init__(self, filename: str = "posts.json") -> None:
        self.filename = filename
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            self.save_posts([])

    def load_posts(self) -> list[SocialPost]:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [post_from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_posts([])
            return []

    def save_posts(self, posts: list[SocialPost]) -> bool:
        try:
            with open(self.filename, "w") as f:
                json.dump([post.to_dict() for post in posts], f, indent=4)
            return True
        except IOError:
            return False

    def add_post(self, post: SocialPost) -> None:
        posts = self.load_posts()
        if any(p.id == post.id for p in posts):
            return
        posts.append(post)
        self.save_posts(posts)

    def update_status(self, post_id: str, new_status: str) -> bool:
        posts = self.load_posts()
        updated = False
        for post in posts:
            if post.id == post_id:
                post.status = new_status
                updated = True
                break
        if updated:
            self.save_posts(posts)
        return updated

    def delete_post(self, post_id: str) -> bool:
        """Wipes a specific post record matching the unique ID from disk storage."""
        posts = self.load_posts()
        initial_length = len(posts)
        posts = [p for p in posts if p.id != post_id]
        
        if len(posts) < initial_length:
            self.save_posts(posts)
            return True
        return False