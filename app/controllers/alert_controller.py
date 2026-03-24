from fastapi import HTTPException
from app.schemas.alert_schema import SOSRequest, SOSResponse
from app.services.firestore_service import firestore_service
from app.services.alert_service import alert_service
from app.utils.logger import logger

class AlertController:
    """Handle emergency SOS alerts from ESP32"""
    
    async def create_sos_alert(self, sos_request: SOSRequest) -> SOSResponse:
        """Process emergency SOS alert - Store in Firestore + Send SMS/Call via Twilio"""
        try:
            alert_data = {
                "patientId": sos_request.patientId,
                "type": sos_request.type,
                "severity": sos_request.severity,
                "location": sos_request.location.model_dump(),
                "doctorNumber": sos_request.doctorNumber,
                "familyNumbers": sos_request.familyNumbers,
            }
            if sos_request.customMessage:
                alert_data["customMessage"] = sos_request.customMessage
            
            # Store alert in Firestore
            alert_id = await firestore_service.store_alert(
                patient_id=sos_request.patientId,
                alert_data=alert_data
            )
            
            # Send SMS + Call to all contacts via Twilio
            actions = alert_service.send_emergency_alerts(
                patient_id=sos_request.patientId,
                alert_type=sos_request.type,
                location=alert_data["location"],
                doctor_number=sos_request.doctorNumber,
                family_numbers=sos_request.familyNumbers,
                custom_message=sos_request.customMessage,
            )
            
            logger.critical(f"🚨 SOS alert {alert_id} processed for patient {sos_request.patientId}")
            
            return SOSResponse(
                success=True,
                message="Emergency alert processed - SMS and Calls sent",
                alertId=alert_id,
                actions_taken=actions
            )
            
        except Exception as e:
            logger.error(f"Error processing SOS alert: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

alert_controller = AlertController()
