from fastapi import HTTPException
from app.schemas.iot_schema import DailyVitalsRequest, DailyVitalsResponse
from app.services.firestore_service import firestore_service
from app.utils.logger import logger

class IoTController:
    """Handle IoT device data ingestion"""
    
    async def receive_daily_vitals(self, vitals: DailyVitalsRequest) -> DailyVitalsResponse:
        """Process and store daily vitals from IoT device"""
        try:
            vitals_dict = vitals.model_dump()
            
            await firestore_service.store_daily_vitals(
                patient_id=vitals.patientId,
                vitals_data=vitals_dict
            )
            
            logger.info(f"Successfully received vitals from IoT device for patient {vitals.patientId}")
            
            return DailyVitalsResponse(
                success=True,
                message="Vitals data received and stored successfully",
                data={"patientId": vitals.patientId, "date": vitals.date}
            )
            
        except Exception as e:
            logger.error(f"Error processing IoT vitals: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to store vitals: {str(e)}")

iot_controller = IoTController()
