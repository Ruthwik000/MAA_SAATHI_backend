import firebase_admin
from firebase_admin import credentials, firestore
from app.config.settings import settings
from app.utils.logger import logger
import json

_db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _db
    try:
        if not firebase_admin._apps:
            # Use credentials from environment variable
            if settings.firebase_credentials_json:
                logger.info("Loading Firebase credentials from environment variable")
                cred_dict = json.loads(settings.firebase_credentials_json)
                cred = credentials.Certificate(cred_dict)
            else:
                raise ValueError("FIREBASE_CREDENTIALS_JSON environment variable not set")
            
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
