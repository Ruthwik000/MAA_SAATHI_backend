import random
from datetime import datetime

class MockDataService:
    """Generate mock vitals data for health check simulation"""
    
    @staticmethod
    def generate_mock_vitals(patient_id: str) -> dict:
        """Generate realistic mock vitals data"""
        return {
            "patientId": patient_id,
            "heartRateAvg": round(random.uniform(60, 100), 1),
            "spo2Avg": round(random.uniform(95, 100), 1),
            "steps": random.randint(3000, 12000),
            "sleepHours": round(random.uniform(6, 9), 1),
            "temperatureAvg": round(random.uniform(36.5, 37.5), 1),
            "date": datetime.utcnow().date().isoformat(),
            "timestamp": datetime.utcnow().isoformat()
        }

mock_data_service = MockDataService()
