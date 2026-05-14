import {
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import type { TelemetryPayload } from "../types/telemetry";

interface Props {
    history: TelemetryPayload[];
}

export function TelemetryChart({ history }: Props) {
    if (!history.length) {
        return (
            <div className="card">
                <h2>Telemetry History</h2>
                <p>Waiting for telemetry...</p>
            </div>
        );
    }

    const chartData = history.map((item) => ({
        time: new Date(item.timestamp).toLocaleTimeString(),
        temperature: item.temperature,
    }));

    return (
        <div className="card chart">
            <h2>Telemetry History</h2>

            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="temperature" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}