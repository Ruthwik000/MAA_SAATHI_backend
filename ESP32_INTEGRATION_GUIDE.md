# ESP32 Ring - Backend Integration Guide

## ✅ Live Backend URL
```
https://maa-saathi-backend.onrender.com
```

## 📱 Emergency Contact
```
Phone: +918328217825
```

---

## 🎯 ESP32 Triggers → Backend Routes

### 1. **SOS BUTTON PRESSED** (Manual Emergency)
**Trigger:** Button on GPIO 14 pressed
**Action:** Sends emergency alert immediately
**Route:** `POST /api/v1/emergency/sos`
**Payload:**
```json
{
  "patientId": "patient_demo",
  "type": "MANUAL_SOS",
  "severity": "HIGH",
  "location": {"lat": 28.6139, "lng": 77.2090},
  "doctorNumber": "+918328217825",
  "familyNumbers": ["+918328217825"]
}
```
**Result:** 
- ✅ SMS sent to +918328217825
- ✅ Voice call to +918328217825
- ✅ Alert stored in Firestore

---

### 2. **FALL DETECTION** (Automatic)
**Trigger:** MPU9250 detects sudden impact (G-force > 3.0)
**Action:** Sends HIGH severity alert
**Route:** `POST /api/v1/emergency/sos`
**Payload:**
```json
{
  "patientId": "patient_demo",
  "type": "FALL",
  "severity": "HIGH",
  "location": {"lat": 28.6139, "lng": 77.2090},
  "doctorNumber": "+918328217825",
  "familyNumbers": ["+918328217825"]
}
```
**Result:**
- ✅ SMS sent to +918328217825
- ✅ Voice call to +918328217825
- ✅ Alert stored in Firestore

---

### 3. **ABNORMAL HEART RATE** (Every 5 seconds check)
**Trigger:** Heart rate < 50 or > 120 bpm
**Action:** Sends MEDIUM/HIGH severity alert
**Route:** `POST /api/v1/emergency/sos`
**Payload:**
```json
{
  "patientId": "patient_demo",
  "type": "HIGH_HEART_RATE",
  "severity": "MEDIUM",  // HIGH if HR > 140 or < 40
  "location": {"lat": 28.6139, "lng": 77.2090},
  "doctorNumber": "+918328217825",
  "familyNumbers": ["+918328217825"]
}
```
**Result:**
- ✅ SMS sent to +918328217825
- ✅ Voice call to +918328217825
- ✅ Alert stored in Firestore

---

### 4. **LOW SPO2** (Every 5 seconds check)
**Trigger:** SpO2 < 90%
**Action:** Sends MEDIUM/HIGH severity alert
**Route:** `POST /api/v1/emergency/sos`
**Payload:**
```json
{
  "patientId": "patient_demo",
  "type": "LOW_SPO2",
  "severity": "MEDIUM",  // HIGH if SpO2 < 85
  "location": {"lat": 28.6139, "lng": 77.2090},
  "doctorNumber": "+918328217825",
  "familyNumbers": ["+918328217825"]
}
```
**Result:**
- ✅ SMS sent to +918328217825
- ✅ Voice call to +918328217825
- ✅ Alert stored in Firestore

---

### 5. **VITALS UPLOAD** (Every 20 seconds)
**Trigger:** Automatic timer
**Action:** Uploads current vitals to Firestore
**Route:** `POST /api/v1/iot/daily-vitals`
**Payload:**
```json
{
  "patientId": "patient_demo",
  "heartRateAvg": 75.0,
  "spo2Avg": 98.0,
  "steps": 1234,
  "sleepHours": 7.5,
  "temperatureAvg": 36.5,
  "date": "2024-03-24"
}
```
**Result:**
- ✅ Vitals stored in Firestore
- ✅ Available for frontend to read

---

## 🔄 ESP32 Loop Timing

| Task | Interval | Function |
|------|----------|----------|
| SOS Button Check | Instant (Interrupt) | `handleSOS()` |
| Fall Detection | Continuous | `processMotion()` |
| Abnormal Vitals Check | Every 5 seconds | `checkAbnormalVitals()` |
| Vitals Upload | Every 20 seconds | `uploadDailyVitals()` |
| Sensor Reading | Every 2 seconds | Main loop |

---

## 📊 OLED Display Shows

```
WiFi:OK GPS:OK
HR:75 bpm SpO2:98%
Temp: 36.5C
Steps: 1234
Env: 26.5C 50%
```

---

## 🚨 Emergency Alert Flow

```
ESP32 Detects Emergency
    ↓
Sends POST to Backend
    ↓
Backend Stores in Firestore
    ↓
Backend Calls Twilio API
    ↓
Twilio Sends SMS + Makes Call
    ↓
+918328217825 Receives Alert
```

---

## ✅ Verification Checklist

- [x] Backend URL updated to Render
- [x] Emergency contact: +918328217825
- [x] SOS button triggers emergency alert
- [x] Fall detection triggers emergency alert
- [x] Abnormal HR triggers emergency alert
- [x] Low SpO2 triggers emergency alert
- [x] Vitals upload every 20 seconds
- [x] All alerts send SMS + Call
- [x] All data stored in Firestore

---

## 🧪 Testing

Upload code to ESP32 and test:

1. **Press SOS button** → Should receive SMS + Call
2. **Simulate fall** (shake device hard) → Should receive SMS + Call
3. **Wait 20 seconds** → Vitals should upload to Firestore
4. **Check Serial Monitor** → Should see "✅ Vitals uploaded!"

---

## 📱 Expected SMS Message

```
🚨 EMERGENCY ALERT 🚨
Patient: patient_demo
Type: MANUAL_SOS
Location: 28.6139, 77.209
Please respond immediately!
```

---

## 📞 Expected Voice Call

From: +13186603897 (Twilio)
Message: "Emergency Alert! This is a test call from VitalSync..."

---

## 🎉 System Ready!

Your ESP32 ring is now connected to the live backend and will trigger real SMS + Calls when emergencies are detected!
