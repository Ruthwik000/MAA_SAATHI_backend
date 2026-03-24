from fastapi import APIRouter
from app.schemas.iot_schema import DailyVitalsRequest, DailyVitalsResponse
from app.controllers.iot_controller import iot_controller

router = APIRouter(prefix="/api/v1/iot", tags=["IoT"])

@router.post("/daily-vitals", response_model=DailyVitalsResponse)
async def receive_daily_vitals(vitals: DailyVitalsRequest):
    """
    Receive daily vitals data from ESP32 IoT device
    
    - Called by ESP32 smart ring
    - Validates and stores vitals data
    - Returns success confirmation
    """
    return await iot_controller.receive_daily_vitals(vitals)
