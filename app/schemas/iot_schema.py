from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class DailyVitalsRequest(BaseModel):
    patientId: str = Field(..., min_length=1, description="Patient unique identifier")
    heartRateAvg: float = Field(..., ge=0, le=300, description="Average heart rate (bpm)")
    spo2Avg: float = Field(..., ge=0, le=100, description="Average SpO2 level (%)")
    steps: int = Field(..., ge=0, description="Total steps count")
    sleepHours: float = Field(..., ge=0, le=24, description="Total sleep hours")
    temperatureAvg: float = Field(..., ge=30, le=45, description="Average temperature (°C)")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

class DailyVitalsResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class VitalsData(BaseModel):
    patientId: str
    heartRateAvg: float
    spo2Avg: float
    steps: int
    sleepHours: float
    temperatureAvg: float
    date: str
    timestamp: str
