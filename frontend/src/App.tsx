import "./App.css";
import { CommandForm } from "./components/CommandForm";
import { Dashboard } from "./components/Dashboard";
import { StatusIndicator } from "./components/StatusIndicator";
import { TelemetryChart } from "./components/TelemetryChart";
import { useWebSocket } from "./hooks/useWebSocket";

function App() {
    const { connected, telemetry, history } = useWebSocket();

    return (
        <div className="app">
            <div className="header">
                <h1>CONTROLLER EMULATOR</h1>
                <StatusIndicator connected={connected} />
            </div>

            <div className="layout">
                <Dashboard telemetry={telemetry} />
                <CommandForm />
            </div>

            <TelemetryChart history={history} />
        </div>
    );
}

export default App;