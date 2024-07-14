from github import Github, Auth
import threading
import uuid

class GitHubAuthManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.github_objects = {}

    def create_github_object(self, token: str, base_url: str = None) -> str:
        with self.lock:
            key_id = str(uuid.uuid4())
            auth = Auth.Token(token)
            github_obj = Github(auth=auth, base_url=base_url) if base_url else Github(auth=auth)
            
            try:
                github_obj.get_user().id
            except Exception as e:
                raise ValueError(f"Invalid API Key: {e}")

            self.github_objects[key_id] = github_obj
            return key_id

    def get_github_object(self, key_id: str) -> Github:
        with self.lock:
            if key_id not in self.github_objects:
                raise ValueError("GitHub object ID does not exist")
            return self.github_objects[key_id]

    def delete_github_object(self, key_id: str):
        with self.lock:
            if key_id not in self.github_objects:
                raise ValueError("GitHub object ID does not exist")
            del self.github_objects[key_id]

# Create a global instance to be used throughout the application
github_auth_manager = GitHubAuthManager()
