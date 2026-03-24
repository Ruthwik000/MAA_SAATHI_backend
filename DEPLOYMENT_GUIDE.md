# VitalSync - Render Deployment Guide

## Quick Deploy to Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `MAA_SAATHI_backend`
4. Configure:
   - **Name**: `vitalsync-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables

In Render dashboard, add these environment variables:

```
DEMO_MODE=false
FIREBASE_CREDENTIALS_PATH=./saathi-f94ab-firebase-adminsdk-fbsvc-27f9b9ab59.json
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_MESSAGING_SERVICE_SID=<your_twilio_messaging_service_sid>
TWILIO_PHONE_NUMBER=<your_twilio_phone_number>
```

### 4. Upload Firebase Credentials

Since Firebase credentials file can't be in git, you have 2 options:

**Option A: Use Environment Variable (Recommended)**
1. Copy content of `saathi-f94ab-firebase-adminsdk-fbsvc-27f9b9ab59.json`
2. In Render, add environment variable:
   - Key: `FIREBASE_CREDENTIALS_JSON`
   - Value: Paste the entire JSON content

**Option B: Use Render Secret Files**
1. In Render dashboard → Settings → Secret Files
2. Add file: `saathi-f94ab-firebase-adminsdk-fbsvc-27f9b9ab59.json`
3. Paste the JSON content

### 5. Deploy

Click "Create Web Service" - Render will automatically deploy!

### 6. Update ESP32 Code

After deployment, update your ESP32 ring code:

```cpp
const char* API_BASE_URL = "https://vitalsync-backend.onrender.com";
```

### 7. Test Deployment

```bash
curl https://vitalsync-backend.onrender.com/health
```

Should return:
```json
{"status":"ok","service":"VitalSync","mode":"production"}
```

## API Endpoints

- **POST** `/api/v1/iot/daily-vitals` - Store vitals from ESP32
- **POST** `/api/v1/emergency/sos` - Emergency alert (SMS + Call)
- **GET** `/health` - Health check

## Troubleshooting

### Firebase Connection Issues
If you see Firebase errors, make sure:
1. Firebase credentials are properly uploaded
2. `DEMO_MODE=false` in environment variables
3. Check Render logs for specific errors

### Twilio Not Working
Verify all Twilio environment variables are set correctly in Render dashboard.

## Free Tier Limits

Render free tier:
- 750 hours/month
- Sleeps after 15 min inactivity
- First request after sleep takes ~30 seconds

For production, upgrade to paid plan ($7/month) for always-on service.
