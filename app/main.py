from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import iot_routes, alert_routes
from app.config.firebase import initialize_firebase
from app.utils.logger import logger
from app.config.settings import settings

app = FastAPI(
    title="VitalSync API",
    description="Smart Health Monitoring System - IoT Ring Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase on startup (skip in demo mode)
@app.on_event("startup")
async def startup_event():
    try:
        if not settings.demo_mode:
            initialize_firebase()
            logger.info("🚀 VitalSync backend started with Firebase")
        else:
            logger.info("🎯 VitalSync backend started in DEMO MODE")
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    mode = "demo" if settings.demo_mode else "production"
    return {"status": "ok", "service": "VitalSync", "mode": mode}

# Include only essential routers
app.include_router(iot_routes.router)  # ESP32 sends vitals here
app.include_router(alert_routes.router)  # ESP32 sends SOS alerts here
