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
            cred = credentials.Certificate(settings.firebase_credentials_path)
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
