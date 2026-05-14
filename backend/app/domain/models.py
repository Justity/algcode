from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.domain.enums import DeviceStatus, DeviceMode, DeviceError


@dataclass
class Telemetry:
    temperature: float
    pressure: float
    voltage: float
    rpm: int
    connection_quality: int


@dataclass
class DeviceState:
    status: DeviceStatus = DeviceStatus.ONLINE
    mode: DeviceMode = DeviceMode.NORMAL
    error: DeviceError | None = None
    telemetry: Telemetry = field(
        default_factory=lambda: Telemetry(
            temperature=42.0,
            pressure=1.2,
            voltage=12.0,
            rpm=1500,
            connection_quality=100,
        )
    )
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))