interface Props {
    connected: boolean;
}

export function StatusIndicator({ connected }: Props) {
    return (
        <div className={`status-badge ${connected ? "connected" : "disconnected"}`}>
            <span className="dot" />
            {connected ? "CONNECTED" : "DISCONNECTED"}
        </div>
    );
}