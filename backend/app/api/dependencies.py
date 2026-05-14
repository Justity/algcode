from app.websocket.manager import WebSocketManager
from app.services.emulator import EmulatorService


websocket_manager = WebSocketManager()
emulator_service = EmulatorService(websocket_manager)


def get_emulator_service() -> EmulatorService:
    return emulator_service


def get_websocket_manager() -> WebSocketManager:
    return websocket_manager