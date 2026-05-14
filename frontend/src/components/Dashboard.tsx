import type { TelemetryPayload } from "../types/telemetry";

interface Props {
    telemetry: TelemetryPayload | null;
}

export function Dashboard({ telemetry }: Props) {
    if (!telemetry) {
        return (
            <div className="card">
                <h2>LIVE TELEMETRY</h2>
                <p>Waiting for telemetry...</p>
            </div>
        );
    }

    const metrics = [
        ["Temperature", `${telemetry.temperature} °C`],
        ["Pressure", `${telemetry.pressure} bar`],
        ["Voltage", `${telemetry.voltage} V`],
        ["RPM", telemetry.rpm],
        ["Connection", `${telemetry.connection_quality}%`],
        ["Status", telemetry.status.toUpperCase()],
        ["Mode", telemetry.mode.toUpperCase()],
        ["Error", telemetry.error ?? "NONE"],
    ];

    return (
        <div className="card">
            <h2>LIVE TELEMETRY</h2>

            <div className="grid">
                {metrics.map(([label, value]) => (
                    <div key={label} className="metric">
                        <div className="metric-label">{label}</div>
                        <div className="metric-value">{value}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}