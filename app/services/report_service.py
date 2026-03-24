from typing import Dict, List
from app.services.firestore_service import firestore_service
from app.utils.logger import logger

class ReportService:
    """Generate health reports from vitals data"""
    
    async def generate_health_report(self, patient_id: str, days: int = 7) -> Dict:
        """Generate aggregated health report"""
        try:
            vitals_list = await firestore_service.get_daily_vitals(patient_id, days)
            
            if not vitals_list:
                return {
                    "patientId": patient_id,
                    "period": f"Last {days} days",
                    "dataPoints": 0,
                    "message": "No data available"
                }
            
            total_heart_rate = sum(v.get('heartRateAvg', 0) for v in vitals_list)
            total_spo2 = sum(v.get('spo2Avg', 0) for v in vitals_list)
            total_steps = sum(v.get('steps', 0) for v in vitals_list)
            total_sleep = sum(v.get('sleepHours', 0) for v in vitals_list)
            total_temp = sum(v.get('temperatureAvg', 0) for v in vitals_list)
            
            count = len(vitals_list)
            
            report = {
                "patientId": patient_id,
                "period": f"Last {days} days",
                "dataPoints": count,
                "avgHeartRate": round(total_heart_rate / count, 1),
                "avgSpo2": round(total_spo2 / count, 1),
                "totalSteps": total_steps,
                "avgStepsPerDay": round(total_steps / count),
                "avgSleepHours": round(total_sleep / count, 1),
                "avgTemperature": round(total_temp / count, 1),
                "vitalsData": vitals_list
            }
            
            logger.info(f"Generated health report for patient {patient_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

report_service = ReportService()
