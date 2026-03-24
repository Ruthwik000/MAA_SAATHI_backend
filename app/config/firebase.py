import firebase_admin
from firebase_admin import credentials, firestore
from app.config.settings import settings
from app.utils.logger import logger
import os
import json

_db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK with Windows path fix"""
    global _db
    try:
        if not firebase_admin._apps:
            # Check if Firebase credentials are in environment variable (for Render)
            firebase_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
            
            if firebase_json:
                # Use credentials from environment variable
                logger.info("Loading Firebase credentials from environment variable")
                cred_dict = json.loads(firebase_json)
                cred = credentials.Certificate(cred_dict)
            else:
                # Use credentials from file (local development)
                cred_path = os.path.abspath(settings.firebase_credentials_path)
                
                # Windows fix: Set GOOGLE_APPLICATION_CREDENTIALS environment variable
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
                
                # Change to the directory containing the credentials file
                original_dir = os.getcwd()
                cred_dir = os.path.dirname(cred_path)
                os.chdir(cred_dir)
                
                try:
                    cred = credentials.Certificate(cred_path)
                    logger.info(f"Loading Firebase credentials from file: {cred_path}")
                finally:
                    # Restore original directory
                    os.chdir(original_dir)
            
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
