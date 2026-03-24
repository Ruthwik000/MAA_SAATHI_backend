from fastapi import APIRouter
from app.schemas.alert_schema import SOSRequest, SOSResponse
from app.controllers.alert_controller import alert_controller

router = APIRouter(prefix="/api/v1", tags=["Alerts"])

@router.post("/emergency/sos", response_model=SOSResponse)
async def create_sos_alert(sos_request: SOSRequest):
    """
    Emergency SOS Alert from ESP32 IoT Ring
    
    - Receives alert with type (MANUAL_SOS, FALL, HIGH_HEART_RATE, etc.)
    - Stores in Firestore
    - Triggers Twilio SMS + Call based on severity:
      - LOW: SMS only
      - MEDIUM/HIGH: SMS + Emergency Call
    """
    return await alert_controller.create_sos_alert(sos_request)
