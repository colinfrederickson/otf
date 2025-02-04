import os
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    CORS_ORIGINS: list = ["http://localhost:5173"]
    API_TITLE: str = "OrangeTheory Fitness API"
    API_DESCRIPTION: str = "API for accessing OrangeTheory Fitness workout data and member information."
    API_VERSION: str = "1.0.0"

settings = Settings()