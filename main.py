from src.lib.cache import CacheEventHandler
from watchdog.observers import Observer

from tabulate import tabulate

def main():
    event_handler = CacheEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/var/cache/apt/archives/", recursive=False)
    observer.start()

    formatted_content = event_handler.get_formatted_content()
    headers = ["Package Name", "Version", "Architecture"]
    print(tabulate(formatted_content, headers=headers, tablefmt="grid"))

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
