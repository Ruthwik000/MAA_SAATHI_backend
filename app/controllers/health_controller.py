import asyncio
from fastapi import HTTPException
from app.services.firestore_service import firestore_service
from app.services.mock_data_service import mock_data_service
from app.services.report_service import report_service
from app.utils.logger import logger

class HealthController:
    """Handle health data retrieval and health check simulation"""
    
    async def get_daily_vitals(self, patient_id: str, days: int = 7):
        """Retrieve daily vitals for a patient"""
        try:
            vitals = await firestore_service.get_daily_vitals(patient_id, days)
            
            return {
                "success": True,
                "patientId": patient_id,
                "count": len(vitals),
                "data": vitals
            }
            
        except Exception as e:
            logger.error(f"Error fetching vitals: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def perform_health_check(self, patient_id: str):
        """Simulate health check (frontend-triggered, not device-triggered)"""
        try:
            logger.info(f"🔍 Health check initiated for patient {patient_id}")
            
            # Simulate sensor reading delay (1-2 seconds)
            await asyncio.sleep(1.5)
            
            # Try to fetch latest stored data
            latest_vitals = await firestore_service.get_latest_vitals(patient_id)
            
            # If no data exists, generate mock data
            if not latest_vitals:
                logger.info(f"No existing data found, generating mock vitals for {patient_id}")
                latest_vitals = mock_data_service.generate_mock_vitals(patient_id)
                
                # Optionally store the mock data
                await firestore_service.store_daily_vitals(patient_id, latest_vitals)
            
            return {
                "success": True,
                "message": "Health check completed",
                "patientId": patient_id,
                "vitals": latest_vitals,
                "simulatedReading": latest_vitals.get('timestamp') is not None
            }
            
        except Exception as e:
            logger.error(f"Error during health check: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_health_report(self, patient_id: str, days: int = 7):
        """Generate comprehensive health report"""
        try:
            report = await report_service.generate_health_report(patient_id, days)
            
            return {
                "success": True,
                "report": report
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

health_controller = HealthController()
