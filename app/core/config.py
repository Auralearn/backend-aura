import os
from typing import List, Union
from pydantic import BaseSettings, field_validator

class Settings(BaseSettings):
    """Application configuration settings.
    
    Handles app settings and  environment variables,
    
    Attributes:
        API_PREFIX: Prefix for all API endpoints
        SECRET_KEY: Secret key for security features
        DATABASE_URL: Connection string for the database
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
    ALLOWED_HOSTS: list[str] = ["*"] 
    
    @field_validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and v:
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]
    
    # Server Information
    SERVER_NAME: str = "FastAPI Server"
    PORT: int = 8000
    HOST: str = "localhost"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()