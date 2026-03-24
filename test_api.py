"""
Test script for VitalSync API endpoints
Run after starting the server: uvicorn app.main:app --reload
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health endpoint"""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_iot_vitals():
    """Test IoT data ingestion"""
    print("\n📡 Testing IoT Vitals Ingestion...")
    
    data = {
        "patientId": "patient_001",
        "heartRateAvg": 75.5,
        "spo2Avg": 98.2,
        "steps": 8500,
        "sleepHours": 7.5,
        "temperatureAvg": 36.8,
        "date": datetime.now().date().isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/iot/daily-vitals", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_get_vitals():
    """Test retrieving vitals"""
    print("\n📊 Testing Get Daily Vitals...")
    
    patient_id = "patient_001"
    response = requests.get(f"{BASE_URL}/api/v1/health/daily-vitals/{patient_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health_check_simulation():
    """Test health check simulation"""
    print("\n🏥 Testing Health Check Simulation...")
    
    patient_id = "patient_001"
    response = requests.post(f"{BASE_URL}/api/v1/health/check/{patient_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health_report():
    """Test health report generation"""
    print("\n📈 Testing Health Report...")
    
    patient_id = "patient_001"
    response = requests.get(f"{BASE_URL}/api/v1/health/report/{patient_id}?days=7")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_sos_alert():
    """Test emergency SOS alert"""
    print("\n🚨 Testing SOS Alert...")
    
    data = {
        "patientId": "patient_001",
        "type": "HIGH_HEART_RATE",
        "severity": "HIGH",
        "location": {
            "lat": 28.6139,
            "lng": 77.2090
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/emergency/sos", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_alerts():
    """Test retrieving alerts"""
    print("\n🔔 Testing Get Alerts...")
    
    patient_id = "patient_001"
    response = requests.get(f"{BASE_URL}/api/v1/alerts/{patient_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("🧪 VitalSync API Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("IoT Vitals", test_iot_vitals),
        ("Get Vitals", test_get_vitals),
        ("Health Check Simulation", test_health_check_simulation),
        ("Health Report", test_health_report),
        ("SOS Alert", test_sos_alert),
        ("Get Alerts", test_get_alerts),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ PASS" if success else "❌ FAIL"))
        except Exception as e:
            print(f"Error: {str(e)}")
            results.append((name, "❌ ERROR"))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    for name, result in results:
        print(f"{result} - {name}")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
