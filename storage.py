# Let's get to work on storage.py 

import json

from requests import post
# Calling in the work already done in the nex file 
from models import post_from_dict 

# The class Storage acts sort of like a filing cabinet for all social media posts.
# It handles reading from and writing to the posts.json file.
class Storage:
    def __init__(self, filename: str = "posts.json") -> None : # Expects a string 'filename' and returns Nothing.""
        self.filename = filename 

    # This method saves a list of posts to the posts.json file.
    # It reads the JSON file and returns a list of SocialPost objects.
    # If the fike doesn't exist yet, return an empty list.(this will usually occur in the first run of the program)
    def load_posts(self) -> List[SocialPost]: # Alaways returns a list of post Objects.
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [post_from_dict(item) for item in data]
        # We expect this error at the first run of the program, so we handle it by returning an empty list.
        except FileNotFoundError:
            return []

        # Custom error for Corrupted JSON files. 
        except json.JSONDecodeError:
            raise RuntimeError("The post(posts.json) is corrupted, you should fix it before adding new posts.")
            # The concern here is that by returning an empty list, we allow for the corrupted file to proceed in error.
            # when we now add posts we run the risk of losing all the post we had in the corrupted file. So we raise an error instead of returning an empty list.
            # print("Warning: posts.json appears corrupted. Starting with empty list.")
            # return []

    # This method takes a list of SocialPost objects and writes them to our JSON file.
    def save_posts(self, posts: list[SocialPost]) -> bool: # It expects a list of post objects and returns True/False for Success/Failure.
        try:
            with open(self.filename, "w") as f:
                # Each post is converted to a dict first using .to_dict() from model.py
                json.dump([post.to_dict() for post in posts], f, indent=4)

        except IOError as e:
            print(f'Error: Could not save posts "{e}"')
            return False
        return True

    # This method adds a single new post to storage.
    # It loads the posts that we already have, appends the new one and then, saves everything back.
    def add_post(self, post: SocialPost) -> None: # It expects a single post Object. it returns nothing but raises an error if need be.
        posts = self.load_posts()
        # This check is simply a safety measure to prevent duplicate ID's. 
        if any(p.id == post.id for p in posts):
            raise ValueError(f'A post with ID "{post.id}" already exists.')
        posts.append(post)
        # Raises IOError if the save fails.
        if not self.save_posts(posts):
            raise IOError(f'Failed to save post "{post.id}" to storage.') # The file may be locked or the disk is full.

    # This method finds a post by it's ID and updates its status.
    # It returns True if the Post was Found and Updated and it returns False if the Post was not Found and Updated.  
    def update_status(self, post_id: str, new_status: str) -> bool: # Both Parameters are string. It returns True/False for Success/Failure.
        posts = self.load_posts()

        posts_by_id = {post.id: post for post in posts}

        if post_id not in posts_by_id:
            print(f"Warning: No post found with ID '{post_id}'")
            return False

        posts_by_id[post_id].status = new_status
        self.save_posts(list(posts_by_id.values()))
        return True