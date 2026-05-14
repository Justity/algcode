from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.enums import DeviceError


class TelemetryResponse(BaseModel):
    temperature: float = Field(..., ge=-100, le=300)
    pressure: float = Field(..., ge=0, le=20)
    voltage: float = Field(..., ge=0, le=100)
    rpm: int = Field(..., ge=0, le=10000)
    connection_quality: int = Field(..., ge=0, le=100)
    error: DeviceError | None = None
    timestamp: datetime