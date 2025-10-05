"""Command-line interface module for LocalSync client."""


def show_help():
    """Display help message for the client."""
    print("Usage: python client.py [options]")
    print("Options:")
    print("  h       Show this help message and exit")
    print("  serve   Start the client application")
    print("  list    List all available packages in the network")
    print("  install <package_name>  Install a package from available servers")