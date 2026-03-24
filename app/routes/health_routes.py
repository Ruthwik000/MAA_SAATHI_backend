from fastapi import APIRouter, Query
from app.controllers.health_controller import health_controller

router = APIRouter(prefix="/api/v1/health", tags=["Health"])

@router.get("/daily-vitals/{patient_id}")
async def get_daily_vitals(
    patient_id: str,
    days: int = Query(default=7, ge=1, le=90, description="Number of days to retrieve")
):
    """
    Retrieve daily vitals for a patient
    
    - Called when user clicks refresh
    - Returns last N days of vitals data
    - Sorted by date descending
    """
    return await health_controller.get_daily_vitals(patient_id, days)

@router.post("/check/{patient_id}")
async def perform_health_check(patient_id: str):
    """
    Simulate health check (frontend-triggered)
    
    - Triggered by "Health Check" button
    - Simulates sensor reading with delay
    - Returns latest or mock vitals data
    - Does NOT call IoT device
    """
    return await health_controller.perform_health_check(patient_id)

@router.get("/report/{patient_id}")
async def get_health_report(
    patient_id: str,
    days: int = Query(default=7, ge=1, le=90, description="Report period in days")
):
    """
    Generate comprehensive health report
    
    - Aggregates vitals over specified period
    - Computes averages and totals
    - Returns structured analytics
    """
    return await health_controller.get_health_report(patient_id, days)
