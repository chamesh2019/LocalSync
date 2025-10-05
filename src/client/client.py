"""Main entry point for LocalSync client application."""
from src.client.cli import show_help
from src.client.network import discover_servers
from src.client.package_manager import install_package, list_packages


def client(*args):
    """Main client function that handles command-line arguments."""
    if "h" in args or "--help" in args:
        show_help()
        return

    if "list" in args:
        servers = discover_servers()
        list_packages(servers)
    
    if "install" in args:
        package_index = args.index("install") + 1
        if package_index < len(args):
            package_name = args[package_index]
            install_package(package_name)
        else:
            print("Error: No package name provided for installation.")
    