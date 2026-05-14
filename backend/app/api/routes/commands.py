from fastapi import APIRouter, Depends

from app.api.dependencies import get_emulator_service
from app.schemas.commands import CommandRequest
from app.schemas.responses import CommandResponse
from app.services.emulator import EmulatorService


router = APIRouter(tags=["commands"])


@router.post("/command", response_model=CommandResponse)
async def execute_command(
    command: CommandRequest,
    emulator: EmulatorService = Depends(get_emulator_service),
):
    message = await emulator.execute_command(command)

    return CommandResponse(
        success=True,
        message=message,
    )