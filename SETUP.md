# VitalSync Backend - Complete Setup Guide

## Prerequisites

- Python 3.10 or higher
- Firebase project with Firestore enabled
- pip package manager

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Firebase Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable Firestore Database
4. Go to Project Settings > Service Accounts
5. Click "Generate New Private Key"
6. Save the JSON file as `serviceAccountKey.json` in project root

### 3. Environment Configuration

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` if needed:
```
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

### 5. Test the API

Visit: `http://localhost:8000/docs` for interactive API documentation

## Quick Test

Test health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "service": "VitalSync"}
```

## Firestore Structure

The backend will automatically create this structure:

```
patients/
  {patientId}/
    dailyVitals/
      {date}/
        - heartRateAvg
        - spo2Avg
        - steps
        - sleepHours
        - temperatureAvg
        - timestamp
    alerts/
      {alertId}/
        - type
        - severity
        - status
        - location
        - timestamp
```

## Troubleshooting

### Firebase Connection Issues
- Verify `serviceAccountKey.json` path is correct
- Check Firebase project has Firestore enabled
- Ensure service account has proper permissions

### Port Already in Use
```bash
uvicorn app.main:app --reload --port 8001
```

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## Production Deployment

For production, use:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Next Steps

1. Test IoT endpoint with sample data
2. Configure frontend to connect to backend
3. Set up monitoring and logging
4. Configure production Firebase rules
