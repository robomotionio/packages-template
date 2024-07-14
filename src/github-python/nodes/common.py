import uuid
import threading

class APIKeyStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.api_keys = {}

    def add_api_key(self, api_key: str) -> str:
        with self.lock:
            key_id = str(uuid.uuid4())
            self.api_keys[key_id] = api_key
            return key_id

    def get_api_key(self, key_id: str) -> str:
        with self.lock:
            if key_id not in self.api_keys:
                raise ValueError("API Key ID does not exist")
            return self.api_keys[key_id]

    def delete_api_key(self, key_id: str):
        with self.lock:
            if key_id not in self.api_keys:
                raise ValueError("API Key ID does not exist")
            del self.api_keys[key_id]

# Create a global instance to be used throughout the application
api_key_store = APIKeyStore()
