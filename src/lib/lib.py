import glob

CACHE_DIR = "/var/cache/apt/archives/"

def get_cached_packages() -> list[str]:
    """Returns a list of cached package files in the APT cache directory."""
    return glob.glob(f"{CACHE_DIR}*.deb")
