import asyncio
import logging
import random
from datetime import datetime, UTC

from app.core.config import settings
from app.domain.enums import (
    CommandType,
    DeviceError,
    DeviceMode,
    DeviceStatus,
)
from app.domain.models import DeviceState
from app.schemas.commands import CommandRequest
from app.schemas.telemetry import TelemetryResponse
from app.websocket.manager import WebSocketManager

logger = logging.getLogger(__name__)


class EmulatorService:
    def __init__(self, websocket_manager: WebSocketManager | None = None):
        self.state = DeviceState()
        self._lock = asyncio.Lock()
        self.websocket_manager = websocket_manager

    async def simulate_delay(self) -> None:
        delay = random.randint(
            settings.min_response_delay_ms,
            settings.max_response_delay_ms,
        )
        await asyncio.sleep(delay / 1000)

    async def start_loop(self) -> None:
        logger.info("emulator loop started")

        while True:
            await asyncio.sleep(settings.telemetry_interval_seconds)

            async with self._lock:
                if self.state.status == DeviceStatus.OFFLINE:
                    continue

                self._update_telemetry()
                self._maybe_inject_random_error()

            await self.broadcast_telemetry()

    async def broadcast_telemetry(self) -> None:
        if not self.websocket_manager:
            return

        async with self._lock:
            telemetry = self.state.telemetry

            payload = {
                "type": "telemetry",
                "payload": {
                    "status": self.state.status.value,
                    "mode": self.state.mode.value,
                    "temperature": telemetry.temperature,
                    "pressure": telemetry.pressure,
                    "voltage": telemetry.voltage,
                    "rpm": telemetry.rpm,
                    "connection_quality": telemetry.connection_quality,
                    "error": self.state.error.value if self.state.error else None,
                    "timestamp": self.state.updated_at.isoformat(),
                },
            }

        await self.websocket_manager.broadcast(payload)

    def _update_telemetry(self) -> None:
        telemetry = self.state.telemetry

        telemetry.temperature = round(
            telemetry.temperature + random.uniform(-1.5, 1.5),
            2,
        )

        telemetry.pressure = round(
            max(0.1, telemetry.pressure + random.uniform(-0.1, 0.1)),
            2,
        )

        telemetry.voltage = round(
            max(0.0, telemetry.voltage + random.uniform(-0.3, 0.3)),
            2,
        )

        telemetry.rpm = max(
            0,
            telemetry.rpm + random.randint(-100, 100),
        )

        telemetry.connection_quality = max(
            0,
            min(
                100,
                telemetry.connection_quality + random.randint(-5, 5),
            ),
        )

        self.state.updated_at = datetime.now(UTC)

    def _maybe_inject_random_error(self) -> None:
        if random.random() > settings.random_error_probability:
            return

        self.state.error = random.choice(list(DeviceError))
        self.state.status = DeviceStatus.ERROR

        logger.warning(
            "random device error injected",
            extra={"error": self.state.error.value},
        )

    async def get_status(self):
        await self.simulate_delay()

        async with self._lock:
            return {
                "status": self.state.status,
                "mode": self.state.mode,
                "updated_at": self.state.updated_at,
            }

    async def get_telemetry(self) -> TelemetryResponse:
        await self.simulate_delay()

        async with self._lock:
            telemetry = self.state.telemetry

            return TelemetryResponse(
                temperature=telemetry.temperature,
                pressure=telemetry.pressure,
                voltage=telemetry.voltage,
                rpm=telemetry.rpm,
                connection_quality=telemetry.connection_quality,
                error=self.state.error,
                timestamp=self.state.updated_at,
            )

    async def execute_command(self, command: CommandRequest) -> str:
        await self.simulate_delay()

        async with self._lock:
            match command.command:
                case CommandType.START:
                    self.state.status = DeviceStatus.ONLINE
                    self.state.error = None
                    self.state.telemetry.rpm = 1500
                    return "device started"

                case CommandType.STOP:
                    self.state.status = DeviceStatus.OFFLINE
                    self.state.telemetry.rpm = 0
                    return "device stopped"

                case CommandType.RESET:
                    self.state = DeviceState()
                    return "device reset"

                case CommandType.SET_MODE:
                    self.state.mode = command.payload.mode
                    return f"mode changed to {self.state.mode.value}"

                case CommandType.INJECT_ERROR:
                    self.state.error = command.payload.error
                    self.state.status = DeviceStatus.ERROR
                    return f"error injected: {self.state.error.value}"

                case _:
                    raise ValueError("unknown command")