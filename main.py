import sys
from src.lib.cache import CacheEventHandler
from watchdog.observers import Observer

from src.server.server import app
from src.client.client import client
import uvicorn

from tabulate import tabulate

def main(*args):
    if "serve" in args:
        event_handler = CacheEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path="/var/cache/apt/archives/", recursive=False)
        observer.start()

        formatted_content = event_handler.get_formatted_content()
        headers = ["Package Name", "Version", "Architecture"]
        print(tabulate(formatted_content, headers=headers, tablefmt="grid"))

        uvicorn.run(app, host="0.0.0.0", port=53456)

        observer.stop()
        observer.join()
    
    else:
        client(*args)

if __name__ == "__main__":
    main(*sys.argv[1:])
