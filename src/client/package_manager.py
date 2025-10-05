"""Package management functions for LocalSync client."""
import platform
from turtle import down
import requests
from tabulate import tabulate

from src.client.network import discover_servers


def is_architecture_compatible(system_arch, package_arch):
    """Check if a package architecture is compatible with the system architecture."""
    # Normalize architectures to lowercase for comparison
    system_arch = system_arch.lower()
    package_arch = package_arch.lower()
    
    # Direct match
    if system_arch == package_arch:
        return True
    
    # Architecture mappings for common variations
    arch_mappings = {
        'x86_64': ['amd64', 'x86-64', 'x64'],
        'amd64': ['x86_64', 'x86-64', 'x64'],
        'i386': ['i686', 'x86'],
        'i686': ['i386', 'x86'],
        'aarch64': ['arm64'],
        'arm64': ['aarch64'],
        'armv7l': ['armhf', 'arm'],
        'armhf': ['armv7l', 'arm'],
    }
    
    # Check if package_arch is compatible with system_arch
    if system_arch in arch_mappings:
        if package_arch in arch_mappings[system_arch]:
            return True
    
    # Check reverse mapping
    if package_arch in arch_mappings:
        if system_arch in arch_mappings[package_arch]:
            return True
    
    # Universal packages (usually marked as 'all' or 'noarch')
    if package_arch in ['all', 'noarch', 'any']:
        return True
    
    return False


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


def fetch_package_details(package_name, servers):
    """Fetch package details from all available servers."""
    package_details = []
    for server in servers:
        try:
            response = requests.get(f"http://{server['ip']}:{server['port']}/api/pkg/{package_name}")
            if response.status_code == 200 and "error" not in response.json():
                for item in response.json():
                    package_details.append((server, item))
        except requests.RequestException as e:
            print(f"Failed to connect to server {server['ip']}:{server['port']}. Error: {e}")
            continue
    return package_details


def filter_compatible_packages(package_details, system_architecture):
    """Filter packages that are compatible with the system architecture."""
    filtered_details = []
    for server, details in package_details:
        if is_architecture_compatible(system_architecture, details['architecture']):
            filtered_details.append((server, details))
    return filtered_details


def display_package_options(filtered_details, all_details=None):
    """Display available package options to the user."""
    if filtered_details:
        print("Compatible packages found:")
        for i, (server, details) in enumerate(filtered_details, 1):
            print(f"{i}. Server: {server['ip']}:{server['port']}, Version: {details['version']}, Architecture: {details['architecture']}")
        return True
    else:
        print("No compatible packages found for your architecture.")
        if all_details:
            print("Available packages (all architectures):")
            for i, (server, details) in enumerate(all_details, 1):
                print(f"{i}. Server: {server['ip']}:{server['port']}, Version: {details['version']}, Architecture: {details['architecture']}")
        return False


def get_user_package_choice(filtered_details):
    """Get user's package selection choice."""
    choice = input("Select a package to install by number (or 'q' to quit): ").strip()
    if choice.lower() == 'q':
        print("Installation aborted by user.")
        return None
    
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(filtered_details):
            return filtered_details[choice_index]
        else:
            print("Invalid selection. Installation aborted.")
            return None
    except ValueError:
        print("Invalid input. Installation aborted.")
        return None


def download_and_install_package(package_name, selected_server, selected_package):
    """Download and install the selected package."""
    print(f"Installing package {package_name} from {selected_server['ip']}:{selected_server['port']}...")
    
    # Construct filename and API endpoint
    filename = f"{package_name}_{selected_package['version']}_{selected_package['architecture']}.deb"
    download_url = f"http://{selected_server['ip']}:{selected_server['port']}/api/download"
    print(f"Downloading {filename} from {download_url}...")
    
    try:
        # Use POST request with filename in body
        response = requests.post(download_url, json={"filename": filename})
        if response.status_code == 200:
            deb_file_path = f"/tmp/{package_name}_{selected_package['version']}_{selected_package['architecture']}.deb"
            with open(deb_file_path, 'wb') as deb_file:
                deb_file.write(response.content)
            print(f"Downloaded package to {deb_file_path}. Installing...")
            
            import os
            result = os.system(f"sudo dpkg -i {deb_file_path}")
            if result == 0:
                print(f"Package {package_name} installed successfully.")
                return True
            else:
                print(f"Failed to install package {package_name}.")
                return False
        else:
            print(f"Failed to download package. HTTP status: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error downloading package: {e}")
        return False


def fallback_apt_install(package_name):
    """Fallback to using apt for package installation."""
    print("Do you want to use apt to install the package? (y/n): ", end="")
    choice = input().strip().lower()
    if choice == 'y':
        import os
        result = os.system(f"sudo apt install {package_name}")
        return result == 0
    else:
        print("Package installation aborted.")
        return False


def install_package(package_name):
    """Install a package from available servers."""
    print(f"Attempting to install package: {package_name}")
    servers = discover_servers()
    
    # Fetch package details from servers
    package_details = fetch_package_details(package_name, servers)

    if package_details:
        print(f"Package {package_name} details found:")
        pc_architecture = platform.machine()
        print(f"Detected architecture: {pc_architecture}")
        
        # Filter packages for compatible architectures
        filtered_details = filter_compatible_packages(package_details, pc_architecture)
        
        # Display package options
        has_compatible_packages = display_package_options(filtered_details, package_details)
        
        if has_compatible_packages:
            # Get user's choice
            selected_package_info = get_user_package_choice(filtered_details)
            if selected_package_info:
                selected_server, selected_package = selected_package_info
                # Download and install the package
                success = download_and_install_package(package_name, selected_server, selected_package)
                if not success:
                    print("Installation failed. You may want to try a different package or use apt.")
    else:
        print(f"No details found for package {package_name} on any server.")
        fallback_apt_install(package_name)

