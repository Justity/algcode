import { useState } from "react";
import { sendCommand } from "../api/commands";

export function CommandForm() {
    const [mode, setMode] = useState("normal");
    const [error, setError] = useState("overheat");
    const [message, setMessage] = useState("");

    async function execute(command: string, payload?: Record<string, string>) {
        try {
            const result = await sendCommand(command, payload);
            setMessage(result.message);
        } catch (err) {
            setMessage(err instanceof Error ? err.message : "Unknown error");
        }
    }

    return (
        <div className="card">
            <h2>Commands</h2>

            <div className="buttons">
                <button onClick={() => execute("start")}>Start</button>
                <button onClick={() => execute("stop")}>Stop</button>
                <button onClick={() => execute("reset")}>Reset</button>
            </div>

            <div className="form-row">
                <select value={mode} onChange={(e) => setMode(e.target.value)}>
                    <option value="normal">Normal</option>
                    <option value="maintenance">Maintenance</option>
                    <option value="safe">Safe</option>
                </select>

                <button
                    onClick={() =>
                        execute("set_mode", {
                            mode,
                        })
                    }
                >
                    Set Mode
                </button>
            </div>

            <div className="form-row">
                <select value={error} onChange={(e) => setError(e.target.value)}>
                    <option value="overheat">Overheat</option>
                    <option value="sensor_failure">Sensor Failure</option>
                    <option value="communication_timeout">Comm Timeout</option>
                    <option value="voltage_drop">Voltage Drop</option>
                </select>

                <button
                    onClick={() =>
                        execute("inject_error", {
                            error,
                        })
                    }
                >
                    Inject Error
                </button>
            </div>

            {message && <p>{message}</p>}
        </div>
    );
}