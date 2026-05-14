from pydantic import BaseModel, model_validator

from app.domain.enums import CommandType, DeviceError, DeviceMode


class CommandPayload(BaseModel):
    mode: DeviceMode | None = None
    error: DeviceError | None = None


class CommandRequest(BaseModel):
    command: CommandType
    payload: CommandPayload | None = None

    @model_validator(mode="after")
    def validate_payload(self):
        if self.command == CommandType.SET_MODE:
            if not self.payload or not self.payload.mode:
                raise ValueError("payload.mode is required for set_mode")

        if self.command == CommandType.INJECT_ERROR:
            if not self.payload or not self.payload.error:
                raise ValueError("payload.error is required for inject_error")

        return self