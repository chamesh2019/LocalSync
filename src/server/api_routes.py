"""API endpoints for LocalSync server."""
from fastapi import FastAPI
import socket
from src.lib.cache import CacheEventHandler
from .network_utils import get_ip_list
from .mdns_service import SERVICE_PORT, is_mdns_registered


def setup_api_routes(app: FastAPI, cache_event_handler: CacheEventHandler):
    """Setup API routes for the FastAPI application."""
    
    @app.get("/api/cache-list")
    def get_cache_list():
        return cache_event_handler.get_formatted_content()

    @app.get("/api/server-info")
    def get_server_info():
        """Endpoint to get current server information"""
        return {
            "hostname": socket.gethostname(),
            "ips": get_ip_list(),
            "port": SERVICE_PORT,
            "package_count": len(cache_event_handler.get_formatted_content()),
            "mdns_registered": is_mdns_registered()
        }


    @app.get("/api/pkg/{package_name}")
    def get_package_info(package_name: str):
        """Endpoint to get information about a specific package"""
        package = cache_event_handler.get_package(package_name)
        if package:
            return package
        return {"error": "Package not found"}