"""
Core configuration for Vortex Hub Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Vortex Hub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Database
    DATABASE_URL: str = "sqlite:///./vortex_hub.db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_PRE_PING: bool = True
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600  # 1 hour
    REFRESH_TOKEN_EXPIRATION: int = 604800  # 7 days
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    ALLOWED_HOSTS: list = ["*"]
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Validate production settings
        if self.ENVIRONMENT == "production":
            if self.DEBUG:
                logger.warning("DEBUG mode enabled in production!")
            if self.JWT_SECRET == "your-secret-key-change-in-production":
                raise ValueError("JWT_SECRET must be set in production!")
            if "localhost" in self.CORS_ORIGINS or "127.0.0.1" in self.CORS_ORIGINS:
                logger.warning("Localhost CORS origins in production - restrict for security")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
