import asyncio
import json
import logging
from fastapi import WebSocket, WebSocketDisconnect


logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        async with self._lock:
            self.connections.add(websocket)

        logger.info(
            "websocket client connected",
            extra={"clients": len(self.connections)},
        )

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self.connections.discard(websocket)

        logger.info(
            "websocket client disconnected",
            extra={"clients": len(self.connections)},
        )

    async def broadcast(self, payload: dict) -> None:
        if not self.connections:
            return

        message = json.dumps(payload, default=str)
        dead_connections = []

        for connection in self.connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                dead_connections.append(connection)
            except Exception:
                logger.exception("websocket send failed")
                dead_connections.append(connection)

        for connection in dead_connections:
            await self.disconnect(connection)