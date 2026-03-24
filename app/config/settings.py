from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Firebase individual fields (easier for Render)
    firebase_project_id: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_client_email: Optional[str] = None
    
    environment: str = "development"
    log_level: str = "INFO"
    demo_mode: bool = True  # Default to demo mode
    
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_messaging_service_sid: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"
        validate_assignment = False

settings = Settings()
