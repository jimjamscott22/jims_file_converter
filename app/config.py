"""
Configuration management for the application.
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    cloudconvert_api_key: str = os.getenv("CLOUDCONVERT_API_KEY", "")
    
    # File Upload Settings
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    max_file_size_bytes: int = max_file_size_mb * 1024 * 1024
    
    # Supported formats
    supported_formats: list = ["jpg", "jpeg", "png", "webp", "gif"]
    
    # Server Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Directories
    temp_dir: Path = BASE_DIR / "temp"
    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"
    
    # CloudConvert API Settings
    cloudconvert_api_url: str = "https://api.cloudconvert.com/v2"
    cloudconvert_sync_api_url: str = "https://sync.api.cloudconvert.com/v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create temp directory if it doesn't exist
        self.temp_dir.mkdir(exist_ok=True)
        
        # Warn if API key is not set
        if not self.cloudconvert_api_key or self.cloudconvert_api_key == "your_api_key_here":
            print("⚠️  WARNING: CloudConvert API key not set in .env file!")
            print("   Get your free API key at: https://cloudconvert.com/dashboard/api/v2/keys")


# Create settings instance
settings = Settings()

