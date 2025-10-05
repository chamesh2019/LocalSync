"""Main entry point for LocalSync server application."""
from .app_config import create_app

# Create the FastAPI application
app = create_app()