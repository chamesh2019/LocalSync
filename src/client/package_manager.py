"""Package management functions for LocalSync client."""
import requests
from tabulate import tabulate

from src.client.network import discover_servers

def list_packages(servers):
    """List all available packages from discovered servers."""
    print("Listing all available packages in the network...")
    print("\nDiscovered Servers:")
    if not servers:
        print("No servers found.")
        return
    
    packages = []
    
    for server in servers:
        available_packages = requests.get(f"http://{server['ip']}:{server['port']}/api/cache-list").json()
        
        for pkg in available_packages:
            packages.append({
                "IP": server["ip"],
                "Package Name": pkg[0],
                "Version": pkg[1],
                "Architecture": pkg[2]
            })
    
    if packages:
        print(tabulate(packages, headers="keys", tablefmt="grid"))
    else:
        print("No packages found on any server.")


def install_package(package_name):
    """Install a package from available servers."""
    print(f"Attempting to install package: {package_name}")
    servers = discover_servers()
    
    if not servers:
        print("No servers found. Cannot install package.")
        print("Do you want to use apt to install the package? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == 'y':
            import os
            os.system(f"sudo apt-get install {package_name}")
        else:
            print("Package installation aborted.")
        return
    
    package_details = []
    for server in servers:
        try:
            response = requests.get(f"http://{server['ip']}:{server['port']}/api/pkg/{package_name}")
            if response.status_code == 200:
                for item in response.json():
                    package_details.append((server, item))
        except requests.RequestException as e:
            print(f"Failed to connect to server {server['ip']}:{server['port']}. Error: {e}")
            continue

    if package_details:
        print(f"Package {package_name} details found:")
        for server, details in package_details:
            print(f"version: {details['version']}, architecture: {details['architecture']}")

    else:
        print(f"No details found for package {package_name}.")

    print(f"Package {package_name} could not be installed from any server.")