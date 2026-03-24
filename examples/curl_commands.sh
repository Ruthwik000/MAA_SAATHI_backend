#!/bin/bash

# VitalSync API - cURL Examples

BASE_URL="http://localhost:8000"

echo "VitalSync API Test Commands"
echo "============================"
echo ""

# 1. Health Check
echo "1. Health Check"
curl -X GET "$BASE_URL/health"
echo -e "\n"

# 2. Send IoT Vitals
echo "2. Send IoT Vitals"
curl -X POST "$BASE_URL/api/v1/iot/daily-vitals" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": "patient_001",
    "heartRateAvg": 75.5,
    "spo2Avg": 98.2,
    "steps": 8500,
    "sleepHours": 7.5,
    "temperatureAvg": 36.8,
    "date": "2024-03-24"
  }'
echo -e "\n"

# 3. Get Daily Vitals
echo "3. Get Daily Vitals"
curl -X GET "$BASE_URL/api/v1/health/daily-vitals/patient_001?days=7"
echo -e "\n"

# 4. Health Check Simulation
echo "4. Health Check Simulation"
curl -X POST "$BASE_URL/api/v1/health/check/patient_001"
echo -e "\n"

# 5. Health Report
echo "5. Health Report"
curl -X GET "$BASE_URL/api/v1/health/report/patient_001?days=7"
echo -e "\n"

# 6. Create SOS Alert
echo "6. Create SOS Alert"
curl -X POST "$BASE_URL/api/v1/emergency/sos" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": "patient_001",
    "type": "HIGH_HEART_RATE",
    "severity": "HIGH",
    "location": {
      "lat": 28.6139,
      "lng": 77.2090
    }
  }'
echo -e "\n"

# 7. Get Alerts
echo "7. Get Alerts"
curl -X GET "$BASE_URL/api/v1/alerts/patient_001"
echo -e "\n"
