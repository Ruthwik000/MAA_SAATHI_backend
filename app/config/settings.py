from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    firebase_credentials_path: str = "./serviceAccountKey.json"
    environment: str = "development"
    log_level: str = "INFO"
    demo_mode: bool = False
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_messaging_service_sid: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
