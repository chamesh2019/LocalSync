"""mDNS service registration and management for LocalSync server."""
from zeroconf import ServiceInfo, Zeroconf
import socket
import threading

SERVICE_TYPE = "_localsync._tcp.local."
SERVICE_PORT = 53456

# Global variables to store zeroconf instance
zeroconf_instance = None
service_info = None
mdns_thread = None


def run_mdns_in_thread(cache_event_handler):
    """Run mDNS registration in a separate thread"""
    global zeroconf_instance, service_info
    from .network_utils import get_ip_list
    
    # Get current package count from cache
    package_count = str(len(cache_event_handler.get_formatted_content()))
    
    desc = {
        'path': '/api/cache-list',
        'package_count': package_count
    }
    hostname = socket.gethostname()
    local_ip = get_ip_list()

    if not local_ip:
        print("No valid IP address found for mDNS registration.")
        return False

    service_info = ServiceInfo(
        SERVICE_TYPE,
        f"{hostname}.{SERVICE_TYPE}",
        addresses=[socket.inet_aton(ip) for ip in local_ip],
        port=SERVICE_PORT,
        properties=desc,
        server=f"{hostname}.local.",
    )

    zeroconf_instance = Zeroconf()
    print(f"Registering mDNS service {service_info.name} at {local_ip}:{SERVICE_PORT}")
    zeroconf_instance.register_service(service_info)
    return True


def mDNS_register(cache_event_handler):
    """Start mDNS registration in a separate thread"""
    global mdns_thread
    mdns_thread = threading.Thread(target=run_mdns_in_thread, args=(cache_event_handler,), daemon=True)
    mdns_thread.start()
    # Give it a moment to register
    threading.Event().wait(0.5)
    return service_info, zeroconf_instance


def mDNS_unregister():
    """Unregister mDNS service"""
    global zeroconf_instance, service_info
    
    if zeroconf_instance and service_info:
        print("Unregistering mDNS service...")
        # Run unregistration in a thread to avoid blocking
        def unregister():
            if zeroconf_instance is not None and service_info is not None:
                zeroconf_instance.unregister_service(service_info)
                zeroconf_instance.close()
        
        thread = threading.Thread(target=unregister, daemon=True)
        thread.start()
        thread.join(timeout=2)  # Wait up to 2 seconds for cleanup
        
        zeroconf_instance = None
        service_info = None


def is_mdns_registered():
    """Check if mDNS service is currently registered"""
    return zeroconf_instance is not None