from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class SOSRequest(BaseModel):
    patientId: str = Field(..., min_length=1)
    type: Literal["FALL", "LOW_SPO2", "HIGH_HEART_RATE", "MANUAL_SOS"]
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    location: Location

class SOSResponse(BaseModel):
    success: bool
    message: str
    alertId: Optional[str] = None
    actions_taken: Optional[list[str]] = None

class AlertData(BaseModel):
    alertId: str
    patientId: str
    type: str
    severity: str
    status: str
    location: dict
    timestamp: str

class AlertUpdateRequest(BaseModel):
    status: Literal["active", "resolved"]
