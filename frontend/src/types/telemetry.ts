export type DeviceStatus = "online" | "offline" | "error";
export type DeviceMode = "normal" | "maintenance" | "safe";

export type DeviceError =
    | "sensor_failure"
    | "overheat"
    | "communication_timeout"
    | "voltage_drop"
    | null;

export interface TelemetryPayload {
    status: DeviceStatus;
    mode: DeviceMode;
    temperature: number;
    pressure: number;
    voltage: number;
    rpm: number;
    connection_quality: number;
    error: DeviceError;
    timestamp: string;
}

export interface WebSocketMessage {
    type: "telemetry";
    payload: TelemetryPayload;
}