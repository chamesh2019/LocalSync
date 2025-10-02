import json 
import os

DATA_DIR = "./"
CONTENT_DIR = f"{DATA_DIR}content/"
LOG_FILE = f"{DATA_DIR}localsync.log"
CONFIG_FILE = f"{DATA_DIR}config.json"

class Config:
    def __init__(self, cache_age=2592000, current_cache=None):
        self.config = json.load(open(CONFIG_FILE)) if os.path.exists(CONFIG_FILE) else {}

    def get(self, key):
        return self.config.get(key)

    def add_to_cache(self, item):
        if "saved_content" not in self.config:
            self.config["saved_content"] = []
        self.config["saved_content"].append(item)
        self.save() 

    def save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_cache(self):
        return self.config.get("saved_content", [])

    def get_cache_dirs(self):
        return self.config.get("cache_dirs", [])

    def get_cache_age(self):
        return self.config.get("cache_age", 2592000)  # Default to 30 days if not set