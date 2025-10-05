import socket
import time
from zeroconf import ServiceBrowser, Zeroconf
from zeroconf import ServiceListener

SERVICE_TYPE = "_localsync._tcp.local."  # Changed to match server

class MyListener(ServiceListener):
    def __init__(self, zeroconf_instance):
        self.zeroconf = zeroconf_instance
        self.discovered_servers = []  # Store discovered servers
        print(f"Listening for service type: {SERVICE_TYPE}")

    def add_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        
        if info:
            address = socket.inet_ntoa(info.addresses[0])
            port = info.port
            
            # Extract server info
            server_info = {
                "name": info.name,
                "ip": address,
                "port": port,
            }
            
            self.discovered_servers.append(server_info)
            
            print("--- SERVER FOUND ---")
            print(f"Name: {info.name}")
            print(f"Address: {address}:{port}")

    def remove_service(self, zc, type_, name):
        print(f"Service removed: {name}")
        # Remove from discovered servers list
        self.discovered_servers = [s for s in self.discovered_servers if s["name"] != name]

def run_client_mdns():
    zeroconf = Zeroconf()
    listener = MyListener(zeroconf)
    
    ServiceBrowser(zeroconf, SERVICE_TYPE, listener)
    
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
        print("Client shut down.")

    return listener.discovered_servers  # Return the discovered servers

if __name__ == "__main__":
    run_client_mdns()