from typing import Optional
from app.services.twilio_service import get_twilio_service
from app.utils.logger import logger


class AlertService:
    """Handle emergency alerts - send SMS and Call directly via Twilio"""

    @staticmethod
    def _format_emergency_message(patient_id: str, alert_type: str, location: dict) -> str:
        """Format emergency message for SMS/Call"""
        return (
            f"🚨 EMERGENCY ALERT 🚨\n"
            f"Patient: {patient_id}\n"
            f"Type: {alert_type}\n"
            f"Location: {location['lat']}, {location['lng']}\n"
            f"Please respond immediately!"
        )

    def send_emergency_alerts(
        self,
        patient_id: str,
        alert_type: str,
        location: dict,
        doctor_number: Optional[str] = None,
        family_numbers: Optional[list[str]] = None,
        custom_message: Optional[str] = None,
    ) -> list[str]:
        """Send SMS + Call to all contacts immediately"""
        actions: list[str] = []
        
        # Build recipient list
        recipients = []
        if doctor_number:
            recipients.append(doctor_number)
        if family_numbers:
            recipients.extend(family_numbers)
        
        # Remove duplicates
        recipients = list(set(recipients))

        if not recipients:
            logger.warning(f"No emergency contacts for patient {patient_id}")
            return ["No emergency contacts configured"]

        message = custom_message or self._format_emergency_message(
            patient_id=patient_id,
            alert_type=alert_type,
            location=location,
        )

        try:
            twilio_service = get_twilio_service()
        except RuntimeError as exc:
            logger.error(f"Twilio configuration error: {str(exc)}")
            return [f"Notification failed: {str(exc)}"]

        # Send SMS to all contacts
        sms_sent = 0
        sms_failed = 0
        for phone in recipients:
            try:
                result = twilio_service.send_sms(phone, message)
                if result.status == "success":
                    sms_sent += 1
                    logger.info(f"SMS sent to {phone}")
                else:
                    sms_failed += 1
                    logger.error(f"SMS failed to {phone}: {result.error}")
            except Exception as e:
                sms_failed += 1
                logger.error(f"SMS error to {phone}: {str(e)}")

        # Make calls to all contacts
        call_sent = 0
        call_failed = 0
        for phone in recipients:
            try:
                result = twilio_service.make_call(phone, message)
                if result.status == "success":
                    call_sent += 1
                    logger.info(f"Call initiated to {phone}")
                else:
                    call_failed += 1
                    logger.error(f"Call failed to {phone}: {result.error}")
            except Exception as e:
                call_failed += 1
                logger.error(f"Call error to {phone}: {str(e)}")

        actions.append(f"SMS sent: {sms_sent}, failed: {sms_failed}")
        actions.append(f"Calls initiated: {call_sent}, failed: {call_failed}")
        
        logger.critical(
            f"🚨 Emergency alert processed for {patient_id}: {alert_type} | "
            f"SMS: {sms_sent}/{len(recipients)}, Calls: {call_sent}/{len(recipients)}"
        )
        
        return actions


alert_service = AlertService()
