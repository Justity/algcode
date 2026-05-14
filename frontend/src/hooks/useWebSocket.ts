import { useEffect, useRef, useState } from "react";
import type { TelemetryPayload, WebSocketMessage } from "../types/telemetry";

const WS_URL = "ws://localhost:8000/ws";

export function useWebSocket() {
    const [connected, setConnected] = useState(false);
    const [telemetry, setTelemetry] = useState<TelemetryPayload | null>(null);
    const [history, setHistory] = useState<TelemetryPayload[]>([]);

    const wsRef = useRef<WebSocket | null>(null);
    const reconnectRef = useRef<number>();
    const heartbeatRef = useRef<number>();

    useEffect(() => {
        function connect() {
            const ws = new WebSocket(WS_URL);
            wsRef.current = ws;

            ws.onopen = () => {
                setConnected(true);

                heartbeatRef.current = window.setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send("ping");
                    }
                }, 10000);
            };

            ws.onmessage = (event) => {
                try {
                    const data: WebSocketMessage = JSON.parse(event.data);

                    if (data.type !== "telemetry") return;

                    setTelemetry(data.payload);

                    setHistory((prev) => [...prev.slice(-29), data.payload]);
                } catch (err) {
                    console.error("ws parse error", err);
                }
            };

            ws.onclose = () => {
                setConnected(false);

                reconnectRef.current = window.setTimeout(() => {
                    connect();
                }, 2000);
            };

            ws.onerror = (err) => {
                console.error(err);
                ws.close();
            };
        }

        connect();

        return () => {
            wsRef.current?.close();

            if (reconnectRef.current) {
                clearTimeout(reconnectRef.current);
            }

            if (heartbeatRef.current) {
                clearInterval(heartbeatRef.current);
            }
        };
    }, []);

    return {
        connected,
        telemetry,
        history,
    };
}