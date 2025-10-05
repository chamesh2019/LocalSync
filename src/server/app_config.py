"""Application configuration and lifecycle management for LocalSync server."""
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import asyncio

from src.lib.cache import CacheEventHandler
from .mdns_service import mDNS_register, mDNS_unregister
from .api_routes import setup_api_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    print("Starting LocalSync server...")
    
    # Get cache event handler from app state
    cache_event_handler = app.state.cache_event_handler
    
    # Run mDNS registration in executor to avoid blocking
    loop = asyncio.get_event_loop()
    service_info, _ = await loop.run_in_executor(None, lambda: mDNS_register(cache_event_handler))
    
    if service_info:
        print("mDNS service registered successfully")
    else:
        print("Failed to register mDNS service")
    
    yield
    
    print("Shutting down LocalSync server...")
    await loop.run_in_executor(None, mDNS_unregister)
    print("Server shutdown complete")


def create_app():
    """Create and configure the FastAPI application."""
    app = FastAPI(lifespan=lifespan)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="content"), name="static")

    # Initialize cache event handler
    cache_event_handler = CacheEventHandler()
    app.state.cache_event_handler = cache_event_handler
    
    # Setup API routes
    setup_api_routes(app, cache_event_handler)
    
    return app