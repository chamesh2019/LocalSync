"""API endpoints for LocalSync server."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import socket
import os
from src.lib.cache import CacheEventHandler
from .network_utils import get_ip_list
from .mdns_service import SERVICE_PORT, is_mdns_registered


class FileRequest(BaseModel):
    """Request model for file download."""
    filename: str


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

    @app.post("/api/download")
    def download_file(file_request: FileRequest):
        """Download a file by filename provided in POST request body."""
        filename = file_request.filename
        
        # Validate filename (basic security check)
        if not filename or '..' in filename or filename.startswith('/'):
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        # Construct file path
        file_path = os.path.join("content", filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )