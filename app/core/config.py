import os
from typing import List, Union
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings.
    
    Attributes:
        API_PREFIX: Prefix for all API endpoints
        SECRET_KEY: Secret key for security features
        DATABASE_URL: Connection string for the database
        CORS_ALLOW_ORIGINS:List of allowed origins for CORS
        ALLOWED_HOSTS: List of allowed hosts for CORS
        SERVER_NAME: Name identifier for the server
        PORT: Port number the server runs on
        HOST: Hostname the server binds to
    """
    # API settings
    API_PREFIX: str = "/api"
    
    # Database settings
    DATABASE_URL: str = ""
    
    # CORS and allowed hosts
    CORS_ALLOW_ORIGINS: list[str] = ["*"] 
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"] 
    
    # Server Information
    SERVER_NAME: str = "FastAPI Server"
    PORT: int = 8000
    HOST: str = "localhost"
    
    # Model API KEY
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()