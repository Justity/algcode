from datetime import datetime

from pydantic import BaseModel

from app.domain.enums import DeviceMode, DeviceStatus


class StatusResponse(BaseModel):
    status: DeviceStatus
    mode: DeviceMode
    updated_at: datetime


class CommandResponse(BaseModel):
    success: bool
    message: str