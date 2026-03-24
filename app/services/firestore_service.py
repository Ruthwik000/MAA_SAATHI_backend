from datetime import datetime
from typing import List, Optional, Dict
from app.config.settings import settings
from app.utils.logger import logger
import uuid

# In-memory storage for demo mode
_demo_storage = {
    "vitals": {},
    "alerts": {}
}

class FirestoreService:
    def __init__(self):
        self.demo_mode = settings.demo_mode
        if not self.demo_mode:
            from app.config.firebase import get_db
            self.db = get_db()
        else:
            self.db = None
            logger.info("🎯 DEMO MODE: Using in-memory storage (no Firebase connection)")
    
    async def store_daily_vitals(self, patient_id: str, vitals_data: dict) -> bool:
        """Store daily vitals in Firestore or demo storage"""
        try:
            vitals_data = {
                **vitals_data,
                'patientId': patient_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            if self.demo_mode:
                # Demo mode: store in memory
                if patient_id not in _demo_storage["vitals"]:
                    _demo_storage["vitals"][patient_id] = []
                _demo_storage["vitals"][patient_id].append(vitals_data)
                logger.info(f"📝 DEMO: Stored vitals for patient {patient_id}")
                return True
            
            from app.config.firebase_schema import validate_firestore_document
            validate_firestore_document('patientDailyVitals', vitals_data)
            doc_ref = self.db.collection('patients').document(patient_id)\
                .collection('dailyVitals').document(vitals_data['date'])
            doc_ref.set(vitals_data)
            logger.info(f"Stored vitals for patient {patient_id} on {vitals_data['date']}")
            return True
        except Exception as e:
            logger.error(f"Error storing vitals: {str(e)}")
            raise
    
    async def get_daily_vitals(self, patient_id: str, days: int = 7) -> List[Dict]:
        """Fetch daily vitals for last N days"""
        try:
            if self.demo_mode:
                # Demo mode: return from memory
                vitals = _demo_storage["vitals"].get(patient_id, [])
                logger.info(f"📝 DEMO: Retrieved {len(vitals)} vitals for patient {patient_id}")
                return vitals[-days:]
            
            vitals_ref = self.db.collection('patients').document(patient_id)\
                .collection('dailyVitals')
            
            docs = vitals_ref.order_by('date', direction='DESCENDING').limit(days).stream()
            
            vitals_list = []
            for doc in docs:
                data = doc.to_dict()
                data['date'] = doc.id
                vitals_list.append(data)
            
            logger.info(f"Retrieved {len(vitals_list)} vitals records for patient {patient_id}")
            return vitals_list
        except Exception as e:
            logger.error(f"Error fetching vitals: {str(e)}")
            return []
    
    async def get_latest_vitals(self, patient_id: str) -> Optional[Dict]:
        """Get most recent vitals record"""
        try:
            if self.demo_mode:
                # Demo mode: return latest from memory
                vitals = _demo_storage["vitals"].get(patient_id, [])
                return vitals[-1] if vitals else None
            
            vitals_ref = self.db.collection('patients').document(patient_id)\
                .collection('dailyVitals')
            
            docs = vitals_ref.order_by('date', direction='DESCENDING').limit(1).stream()
            
            for doc in docs:
                data = doc.to_dict()
                data['date'] = doc.id
                return data
            
            return None
        except Exception as e:
            logger.error(f"Error fetching latest vitals: {str(e)}")
            return None
    
    async def store_alert(self, patient_id: str, alert_data: dict) -> str:
        """Store emergency alert"""
        try:
            alert_id = str(uuid.uuid4())
            alert_data = {
                **alert_data,
                'patientId': patient_id,
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'active'
            }
            
            if self.demo_mode:
                # Demo mode: store in memory
                if patient_id not in _demo_storage["alerts"]:
                    _demo_storage["alerts"][patient_id] = []
                alert_data['alertId'] = alert_id
                _demo_storage["alerts"][patient_id].append(alert_data)
                logger.info(f"🚨 DEMO: Stored alert {alert_id} for patient {patient_id}")
                logger.info(f"   Type: {alert_data.get('type')}, Severity: {alert_data.get('severity')}")
                logger.info(f"   Location: {alert_data.get('location')}")
                return alert_id
            
            from app.config.firebase_schema import validate_firestore_document
            validate_firestore_document('patientAlerts', alert_data)
            
            doc_ref = self.db.collection('patients').document(patient_id)\
                .collection('alerts').document(alert_id)
            doc_ref.set(alert_data)
            
            logger.info(f"Stored alert {alert_id} for patient {patient_id}")
            return alert_id
        except Exception as e:
            logger.error(f"Error storing alert: {str(e)}")
            raise
    
    async def get_alerts(self, patient_id: str) -> List[Dict]:
        """Fetch all alerts for a patient"""
        try:
            if self.demo_mode:
                # Demo mode: return from memory
                alerts = _demo_storage["alerts"].get(patient_id, [])
                logger.info(f"📝 DEMO: Retrieved {len(alerts)} alerts for patient {patient_id}")
                return alerts
            
            alerts_ref = self.db.collection('patients').document(patient_id)\
                .collection('alerts')
            
            docs = alerts_ref.order_by('timestamp', direction='DESCENDING').stream()
            
            alerts_list = []
            for doc in docs:
                data = doc.to_dict()
                data['alertId'] = doc.id
                alerts_list.append(data)
            
            logger.info(f"Retrieved {len(alerts_list)} alerts for patient {patient_id}")
            return alerts_list
        except Exception as e:
            logger.error(f"Error fetching alerts: {str(e)}")
            return []
    
    async def update_alert_status(self, patient_id: str, alert_id: str, status: str) -> bool:
        """Update alert status"""
        try:
            if self.demo_mode:
                # Demo mode: update in memory
                alerts = _demo_storage["alerts"].get(patient_id, [])
                for alert in alerts:
                    if alert.get('alertId') == alert_id:
                        alert['status'] = status
                        logger.info(f"📝 DEMO: Updated alert {alert_id} status to {status}")
                        return True
                return False
            
            from app.config.firebase_schema import validate_firestore_document
            validate_firestore_document('patientAlerts', {'status': status}, partial=True)
            doc_ref = self.db.collection('patients').document(patient_id)\
                .collection('alerts').document(alert_id)
            
            doc = doc_ref.get()
            if not doc.exists:
                return False
            
            doc_ref.update({'status': status})
            logger.info(f"Updated alert {alert_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating alert: {str(e)}")
            raise

firestore_service = FirestoreService()
