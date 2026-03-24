import firebase_admin
from firebase_admin import credentials, firestore
from app.config.settings import settings
from app.utils.logger import logger

_db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _db
    try:
        if not firebase_admin._apps:
            # Build credentials from individual environment variables
            if settings.firebase_project_id and settings.firebase_private_key and settings.firebase_client_email:
                logger.info("Loading Firebase credentials from environment variables")
                
                # Build credential dict
                cred_dict = {
                    "type": "service_account",
                    "project_id": settings.firebase_project_id,
                    "private_key": settings.firebase_private_key.replace('\\n', '\n'),  # Fix newlines
                    "client_email": settings.firebase_client_email,
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
                
                cred = credentials.Certificate(cred_dict)
            else:
                raise ValueError("Firebase credentials not configured in environment variables")
            
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully")
                
        _db = firestore.client()
        return _db
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise

def get_db():
    """Get Firestore database instance"""
    global _db
    if _db is None:
        _db = initialize_firebase()
    return _db
