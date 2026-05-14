# Windows Run Instructions

## Requirements
Installed software:

- Python 3.11+
- Node.js 18+
- npm

Check versions:

```powershell
py -3.11 --version
node --version
npm --version
```

---

## Backend запуск

Open PowerShell in project root:

```powershell
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend endpoints:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Frontend запуск

Open another PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Note: if port 5173 is already busy, Vite will automatically choose another one.

---

## Cross-platform compatibility

The project is cross-platform.

Backend:
- FastAPI
- Python standard libraries
- no Windows-specific APIs

Frontend:
- React
- TypeScript
- Vite
- browser-based WebSocket/fetch APIs

Supported platforms:
- Windows
- Linux
- macOS

Only runtime requirements are Python and Node.js.

---

# Selected Communication Protocol

The application uses two communication mechanisms:

## REST API

REST is used for request/response operations where the client explicitly interacts with the controller.

Used for:
- querying current device status
- querying telemetry snapshot
- sending control commands

Endpoints:

```http
GET /api/status
GET /api/parameters
POST /api/command
```

Example command request:

```json
{
  "command": "set_mode",
  "payload": {
    "mode": "maintenance"
  }
}
```

Reason for REST:
- simple synchronous command execution
- clear request/response semantics
- easy testing via Swagger/Postman/curl

---

## WebSocket

WebSocket is used for real-time telemetry streaming.

Endpoint:

```text
/ws
```

Message format:

```json
{
  "type": "telemetry",
  "payload": {
    "status": "online",
    "mode": "normal",
    "temperature": 42.1,
    "pressure": 1.2,
    "voltage": 12.4,
    "rpm": 1530,
    "connection_quality": 98,
    "error": null,
    "timestamp": "2026-05-14T12:00:00Z"
  }
}
```

Frontend sends heartbeat ping messages periodically to keep the connection active.

Reason for WebSocket:
- low-latency real-time updates
- efficient server push model
- suitable for telemetry monitoring dashboards

---

# Architecture

The application follows a layered architecture with separation of concerns.

## Backend Architecture

Layers:

### API Layer
Responsible for:
- REST endpoint handling
- request validation
- response serialization
- HTTP exception handling

Components:
- routes
- dependencies
- websocket endpoint

---

### Service Layer
Responsible for business logic.

Components:
- EmulatorService
- command execution
- telemetry generation
- random fault simulation
- artificial response delays

---

### Domain Layer
Represents device state and business entities.

Components:
- device state
- telemetry model
- enums for status, commands, modes, errors

---

### Infrastructure Layer
Technical supporting components.

Components:
- WebSocket connection manager
- structured logging
- configuration

---

Backend flow:

```text
Client Request
    ↓
FastAPI Route
    ↓
Validation (Pydantic)
    ↓
Service Layer
    ↓
Device State Update / Telemetry Generation
    ↓
Response / WebSocket Broadcast
```

---

## Frontend Architecture

Frontend is separated into logical layers.

### Components
UI rendering only:
- Dashboard
- TelemetryChart
- CommandForm
- StatusIndicator

---

### Hooks
Stateful logic:

- useWebSocket
- reconnect logic
- heartbeat
- telemetry history management

---

### API Layer
REST communication:

- command requests

---

### Types
Shared TypeScript contracts:

- telemetry payload
- websocket messages
- device enums

---

Frontend flow:

```text
WebSocket / REST
    ↓
Hook / API Layer
    ↓
State Update
    ↓
React Components
    ↓
UI Rendering
```