from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    firebase_credentials_path: str = "./serviceAccountKey.json"
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
