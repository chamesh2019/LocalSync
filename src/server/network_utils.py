"""Network utility functions for LocalSync server."""
import netifaces  # type: ignore


def get_ip_list():
    """Get list of non-loopback IP addresses for all network interfaces."""
    ips = []
    for interface in netifaces.interfaces():
        if_addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in if_addresses:
            for link in if_addresses[netifaces.AF_INET]:
                ip = link.get('addr')
                if ip and not ip.startswith("127."):
                    ips.append(ip)
    return ips