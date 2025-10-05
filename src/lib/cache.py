import os
import glob
import shutil

from watchdog.events import FileSystemEventHandler

from src.lib.data import CONTENT_DIR
from src.lib.data import Config
from src.lib.logger import Logger


logger = Logger("CacheEventHandler")

class CacheEventHandler(FileSystemEventHandler):
    """Handles events in the cache directory."""

    def __init__(self):
        """Initializes the event handler."""    
        print("Initializing CacheEventHandler")
        super().__init__()

        cache_file_list = []

        for cache_dir in Config().get_cache_dirs():
            cache_file_list.extend(glob.glob(os.path.join(cache_dir, "*.deb")))

        logger.info(f"Found {len(cache_file_list)} cache files")

        if not os.path.exists(CONTENT_DIR):
            logger.info(f"Creating content directory at {CONTENT_DIR}")
            os.makedirs(CONTENT_DIR)
            logger.info(f"Content directory created at {CONTENT_DIR}")

        for file_path in cache_file_list:
            cache = Config().get_cache()
            if file_path not in cache:
                result = shutil.copy(file_path, CONTENT_DIR)
                if result: 
                    Config().add_to_cache(file_path)
                    logger.info(f"Copied {file_path} to {CONTENT_DIR}")
                else:
                    logger.error(f"Failed to copy {file_path} to {CONTENT_DIR}")


    def on_created(self, event):
        if event.is_directory:
            return
        
        if str(event.src_path).endswith(".deb"):
            os.system(f"cp {event.src_path} {CONTENT_DIR}")
            logger.info(f"New cache file detected and copied: {event.src_path}")
            Config().add_to_cache(event.src_path)

    def get_formatted_content(self):
        items = Config().get_cache()
        formatted = [
            os.path.basename(item).replace(".deb", "").split("_") for item in items
        ]
        return formatted
    
    def get_package(self, package_name):
        items = Config().get_cache()
        packages = []
        for item in items:
            parts = os.path.basename(item).replace(".deb", "").split("_")
            if parts[0] == package_name:
                packages.append({
                    "name": parts[0],
                    "version": parts[1],
                    "architecture": parts[2],
                })
        return packages if packages else []

    
            
