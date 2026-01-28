"""
Configuration file for the Background Remover API.
This file loads environment variables and provides default values.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings class.
    Stores all configuration values used across the application.
    """
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # File upload limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
    MAX_IMAGE_WIDTH: int = int(os.getenv("MAX_IMAGE_WIDTH", "1024"))
    
    # API metadata
    API_TITLE: str = os.getenv("API_TITLE", "Background Remover API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = """
    🎨 Background Remover API
    
    Remove backgrounds from images using AI-powered U²-Net model.
    
    **Features:**
    - Upload JPG/PNG images
    - Automatic background removal
    - Returns PNG with transparent background
    - Auto-resize large images
    - Fast processing
    """
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}


# Create a global settings instance
settings = Settings()