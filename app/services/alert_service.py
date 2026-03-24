from app.utils.logger import logger

class AlertService:
    """Handle emergency alert actions based on severity"""
    
    def send_sms(self, patient_id: str, alert_type: str, location: dict):
        """Simulate sending SMS alert"""
        logger.info(f"📱 SMS sent for patient {patient_id} - Alert: {alert_type} at ({location['lat']}, {location['lng']})")
        return "SMS sent"
    
    def make_call(self, patient_id: str, alert_type: str):
        """Simulate making emergency call"""
        logger.warning(f"📞 Emergency call initiated for patient {patient_id} - Alert: {alert_type}")
        return "Emergency call initiated"
    
    def process_alert(self, severity: str, patient_id: str, alert_type: str, location: dict) -> list:
        """Process alert based on severity level"""
        actions = []
        
        if severity == "LOW":
            self.send_sms(patient_id, alert_type, location)
            actions.append("SMS sent")
        
        elif severity == "MEDIUM":
            self.send_sms(patient_id, alert_type, location)
            actions.extend(["SMS sent", "Event logged"])
            logger.info(f"Medium severity alert logged for patient {patient_id}")
        
        elif severity == "HIGH":
            self.send_sms(patient_id, alert_type, location)
            self.make_call(patient_id, alert_type)
            actions.extend(["SMS sent", "Emergency call initiated", "High priority alert"])
            logger.critical(f"🚨 HIGH SEVERITY alert for patient {patient_id}")
        
        return actions

alert_service = AlertService()
