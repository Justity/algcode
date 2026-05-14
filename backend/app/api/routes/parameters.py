from fastapi import APIRouter, Depends

from app.api.dependencies import get_emulator_service
from app.schemas.telemetry import TelemetryResponse
from app.services.emulator import EmulatorService


router = APIRouter(tags=["parameters"])


@router.get("/parameters", response_model=TelemetryResponse)
async def get_parameters(
    emulator: EmulatorService = Depends(get_emulator_service),
):
    return await emulator.get_telemetry()