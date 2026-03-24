# VitalSync - Smart Health Monitoring Backend

IoT Ring health monitoring system with emergency alert capabilities.

## Features

- **IoT Vitals Storage**: ESP32 ring sends health data → stored in Firestore
- **Emergency SOS Alerts**: Automatic SMS + Call alerts via Twilio

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure `.env`:
```env
DEMO_MODE=true
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_MESSAGING_SERVICE_SID=your_messaging_service_sid
```

3. Run server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### 1. Store IoT Vitals
```
POST /api/v1/iot/daily-vitals
```
ESP32 sends health data (heart rate, SpO2, temperature, steps, etc.)

### 2. Emergency SOS Alert
```
POST /api/v1/emergency/sos
```
Triggers SMS + Call to doctor and family contacts

## ESP32 Configuration

Update WiFi and server in `ringcode.c++`:
```cpp
const char* WIFI_SSID = "Hotspot";
const char* WIFI_PASSWORD = "12345678";
const char* SERVER_URL = "http://192.168.43.1:8000";
```

## Demo Mode

Set `DEMO_MODE=true` to use in-memory storage (no Firebase required).

## Production

Set `DEMO_MODE=false` and configure Firebase credentials path.

## Test

```bash
python test_twilio.py
```
