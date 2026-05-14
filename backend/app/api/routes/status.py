from fastapi import APIRouter, Depends

from app.api.dependencies import get_emulator_service
from app.schemas.responses import StatusResponse
from app.services.emulator import EmulatorService


router = APIRouter(tags=["status"])


@router.get("/status", response_model=StatusResponse)
async def get_status(
    emulator: EmulatorService = Depends(get_emulator_service),
):
    result = await emulator.get_status()
    return StatusResponse(**result)