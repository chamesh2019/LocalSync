"""Network-related functions for LocalSync client."""


def discover_servers():
    """Discover available LocalSync servers on the network."""
    from src.client.service_discovery import run_client_mdns
    clients = run_client_mdns()
    return clients if clients else []